import socket 
import sys
import json
import threading
import sqlite3
import binascii
import os
import tool as tool_db
import datetime

IP 			=""
PORT 		= 8888
LISTEN_MAX 	= 1000
BUFFER_SIZE = 1024
DATA_FILE   = "data.db"
DATA_CONNECTION	= sqlite3.connect(DATA_FILE, check_same_thread=False)
DATA_CURSOR  	= DATA_CONNECTION.cursor()
TOOL_FILE 	    = "tool.db"
TOOL_CONNECTION = sqlite3.connect(TOOL_FILE, check_same_thread=False)
TOOL_CURSOR     = TOOL_CONNECTION.cursor()

LOG_FILE_NAME   = "server.log"
#######################################################################################################################################



#######################################################################################################################################
## database user

def make_auth_token():
	return binascii.hexlify(os.urandom(33)).decode()


def tool_make_models():
	global TOOL_CONNECTION, TOOL_CURSOR
	TOOL_CURSOR.execute("DROP TABLE IF EXISTS Tools")
	TOOL_CURSOR.execute("""CREATE TABLE tools(
		name varchar(50),
		cost BIGINT
		);""")
	TOOL_CONNECTION.commit()

def tool_get_cost(tool):
	global TOOL_CURSOR
	TOOL_CURSOR.execute(f'SELECT cost FORM Tools WHERE name="{tool}"')
	x = TOOL_CURSOR.fetchall()
	return x[0][0]

def data_make_models():
	global DATA_CURSOR, DATA_CONNECTION
	DATA_CURSOR.execute("DROP TABLE IF EXISTS Users")
	create_users= """CREATE TABLE Users(
		username varchar(30) PRIMARY KEY,
		password varchar(30),
		credit BIGINT, 
		auth_token varchar(33)
	);"""
	DATA_CURSOR.execute(create_users)
	DATA_CONNECTION.commit()




def data_set_auth_token(username, auth_token):
	global DATA_CURSOR, DATA_CONNECTION
	DATA_CURSOR.execute(f'UPDATE Users SET auth_token="{auth_token}" WHERE username="{username}"')	
	DATA_CONNECTION.commit()

def data_check_user(username, password):
	global DATA_CURSOR
	DATA_CURSOR.execute(f'SELECT COUNT(username) FROM Users WHERE username="{username}" AND password = "{password}"')
	l = DATA_CURSOR.fetchall()
	if l[0][0] == 1:
		return True
	return False

def data_insert_user(username, password, credit = 0):
	global DATA_CURSOR, DATA_CONNECTION
	DATA_CURSOR.execute(f'INSERT INTO Users VALUES("{username}", "{password}", {credit}, NULL)')
	DATA_CONNECTION.commit()
	
def data_login(username, password):
	global DATA_CURSOR
	DATA_CURSOR.execute(f'SELECT username FROM Users WHERE username="{username}" AND password = "{password}"')
	l = DATA_CURSOR.fetchall()
	if not l:
		return "fail", 0
	auth_token = make_auth_token()
	data_set_auth_token(username, auth_token)
	return "success", auth_token

def data_get_credit(username, password):
	global DATA_CURSOR
	DATA_CURSOR.execute(f'SELECT credit FROM Users WHERE username="{username}" AND password = "{password}"')
	l = DATA_CURSOR.fetchall()
	return l[0][0]
def data_get_credit_by_token(auth_token):
	global DATA_CURSOR
	DATA_CURSOR.execute(f'SELECT credit FROM Users WHERE auth_token="{auth_token}"')
	l = DATA_CURSOR.fetchall()
	return l[0][0]

def data_check_auth_token(auth_token):
	global DATA_CURSOR
	DATA_CURSOR.execute(f'SELECT username FROM Users WHERE auth_token="{auth_token}"')
	l = DATA_CURSOR.fetchall()
	if not l:
		return "fail"
	return "success"
def data_sub_credit(username, password, amount):
	global DATA_CURSOR, DATA_CONNECTION
	DATA_CURSOR.execute(f'UPDATE Users SET credit ={get_credit(username, password) - amount}')
	DATA_CONNECTION.commit()

def data_check_username(username):
	global DATA_CURSOR
	DATA_CURSOR.execute(f'SELECT COUNT(username) FROM Users WHERE username="{username}"')
	l = DATA_CURSOR.fetchall()
	if l[0][0] > 0:
		return True
	return False
def data_sub_credit_by_token(token, amount):
	global DATA_CURSOR, DATA_CONNECTION
	DATA_CURSOR.execute(f'Select create FROM Users WHERE auth_token="{token}"')
	x = fetchall()[0][0]
	DATA_CURSOR.execute(f'UPDATE Users SET credit={x - amount}')
	DATA_CONNECTION.commit()
def data_change_token(token):
	global DATA_CURSOR, DATA_CONNECTION
	auth_token = make_auth_token()
	DATA_CURSOR.execute(f'UPDATE Users SET auth_token="{auth_token}" WHERE auth_token ="{token}"')
	DATA_CONNECTION.commit()
	return auth_token
#######################################################################################################################################

def logging(msg):
	f = open(LOG_FILE_NAME, "a")
	f.write(f'{datetime.datetime.now()} {msg}\n')
	f.close()

#######################################################################################################################################


def app_sign_in(username, password):
	if username == None or password==None:
		return json.dumps({"action":"sign in", "status": "fail"})
	status, auth_token = data_login(username, password)
	if status == "success":
		respone = json.dumps({"action":"sign in", "status":status,"auth_token":auth_token, "credit":data_get_credit(username, password)})
	else:
		respone = json.dumps({"action":"sign in", "status":status})
	return respone

def app_sign_up(username, password):
	if username == None or password == None:
		return json.dumps({"action":"sign up", "status":"fail"})
	status = data_check_username(username)
	print(username)
	print(password)
	print(status)
	if not status: 
		data_insert_user(username, password)
		return json.dumps({"action":"sign up", "status":"success"})
	else:
		return json.dumps({"action":"sign up", "status":"fail"})

def app_use_tool(tool, auth_token):
	if tool == None or auth_token == None:
		return json.dumps({"action":"use tool", "status":"fail"})
	if data_check_auth_token(auth_token) == "fail":
		return json.dumps({"action":"use tool", "status":"fail"})
	money = data_get_credit_by_token(auth_token)
	cost = tool_db.get_cost(tool)
	if( money < cost):
		token = data_change_token(auth_token)
		return json.dumps({"action":"use tool","status":"fail","cost":cost,"money":money,"auth_token":token})
	data_sub_credit_by_token(auth_token)
	money -= cost
	token = data_change_token(auth_token)
	return json.dumps({"action":"use tool","status":"success","money": money, "cost":cost, "auth_token":token})
#######################################################################################################################################

def error(action):
	return json.dumps({"action":action,"status":"fail"})

def handler(lock, confd, addr):
	try:
		request = json.loads(confd.recv(BUFFER_SIZE).decode('utf-8'))
		logging(f'{addr} {str(request)}')
		action = request.get("action")
		if action == "sign in":
			username = request.get("username")
			password = request.get("password")
			lock.acquire()
			response = app_sign_in(username, password).encode("utf-8")
			confd.send(response)
			logging(f'{addr} {str(response)}')
			lock.release()
			return
		if action == "sign up":
			username = request.get("username")
			password = request.get("password")
			lock.acquire()
			response = app_sign_up(username, password).encode("utf-8")
			logging(f'{addr} {str(response)}')
			confd.send(response)
			lock.release()
			return
		if action == "use tool":
			tool = request.get("tool")
			auth_token = request.get("auth_token")
			lock.acquire()
			response = app_use_tool(tool, auth_token).encode("utf-8")
			logging(f'{addr} {str(response)}')
			confd.send(response)
			lock.release()
			return
		lock.acquire()
		confd.send(error("fail"))
		log.release()
	except socket.error as err: 
		print(err)
def start():
	try:
		confd = socket.socket()
	except socket.error: 
		print('error create socket')
		
	confd.bind((IP, PORT))
	confd.listen(LISTEN_MAX)
	print(confd)

	lock = threading.Lock()
	while True:
		c, addr = confd.accept()
		print("Got DATA_CONNECTION from ", addr)
		cliThread = threading.Thread(target=handler, args=(lock, c,addr))
		cliThread.start()

if __name__=="__main__":
	start()