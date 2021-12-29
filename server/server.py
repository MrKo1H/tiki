import socket 
import sys
import json
import threading
import sqlite3
import binascii
import os
import datetime

import Tool
import Data

IP 			=""
PORT 		= 8888
LISTEN_MAX 	= 1000
BUFFER_SIZE = 1024
BILL_CNT    = 0

LOG_FILE_NAME   = "server.log"
#######################################################################################################################################

def logging(msg):
	f = open(LOG_FILE_NAME, "a")
	f.write(f'{datetime.datetime.now()} {msg}\n')
	f.close()

#######################################################################################################################################

def sign_in(username, password):
	if Data.check_user(username, password):
		credit = Data.get_credit(username, password)
		return json.dumps({"action": "sign in", "status": "success", "username":username, "password":password, "money":credit})
	else:
		return json.dumps({"action": "sign in", "status": "fail"   , "username":username, "password":password, "money":0})

def sign_up(username, password, credit):
	if Data.check_user(username, password):
		return json.dumps({"action": "sign up", "status": "fail"   , "username":username, "password":password, "credit":credit})
	else:
		Data.add_user(username, password, credit)
		return json.dumps({"action": "sign up", "status": "success", "username":username, "password":password, "credit":credit})
		
def use_tool(username, password, tool_name):
	global BILL_CNT
	if not Data.check_user(username, password):
		return json.dumps({"action":"use tool", "status":"fail", "username": username, "password": password, "status":"fail"})
	credit = Data.get_credit(username, password)
	cost   = Tool.get_cost(tool_name)
	if( credit >= cost):
		Data.set_credit(username, password, credit - cost)
		BILL_CNT = BILL_CNT + 1
		Data.add_bill_id(BILL_CNT, cost)
		return json.dumps({"action":"use tool", "status": "success", "username":username, "password":password, "BILL ID":BILL_CNT,"payment":cost, "money":credit-cost})
	else:
		return json.dumps({"action":"use tool", "status": "fail"   , "username":username, "password":password, "payment":cost, "money":credit}) 
def log(username, password, bill_id, tool_name):
	logging(f'user name:{username} password:{password} bill id:{bill_id} tool name:{tool_name}')
	return json.dumps({"action":"log", "status":"success"})

def get_info(username, password):
	if Data.check_user(username, password):
		return Data.get_info(username, password)
	else:
		return json.dumps({"action": "get info", "username":username, "password":password, "status":"fail"})

def refund(username, password, bill_id):
	if not Data.check_user(username, password):
		return json.dumps({"action":"refund", "username":username, "password":password, "status":"fail"})
	if not Data.check_bill_id(bill_id):
		return json.dumps({"action":"refund", "username":username, "password":password, "status":"fail"})
	Data.refund_bill_id(username, password, bill_id)
	credit = Data.get_credit(username, password)
	return json.dumps({"action":"refund", "username":username, "password":password, "money": credit, "status":"success"})

#######################################################################################################################################

def error(action):
	return json.dumps({"action":action,"status":"fail"})

def handler(lock, confd, addr):
	try:
		request = json.loads(confd.recv(BUFFER_SIZE).decode('utf-8'))
		logging(request)
		action = request.get("action")
		username = request.get("username")
		password = request.get("password")
		if action == "sign in":
			lock.acquire()
			response = sign_in(username, password)
			confd.send(response.encode('utf-8'))
			confd.close()
			logging(response)
			lock.release()
			return
		if action == "sign up":
			lock.acquire()
			credit = request.get("credit")
			response =sign_up(username, password, credit)
			confd.send(response.encode('utf-8'))
			confd.close()
			logging(response)
			lock.release()
			return
		if action == "use tool":
			tool_name = request.get("tool name")
			lock.acquire()
			response = use_tool(username, password, tool_name)
			confd.send(response.encode('utf-8'))
			confd.close()
			logging(response)
			lock.release()
			return
		if action == "log":
			bill_id  = request.get("bill id")
			tool_name= request.get("tool name")
			lock.acquire()
			response = log(username, password, bill_id, tool_name)
			confd.send(response.encode('utf-8'))
			confd.close()
			logging(response)
			lock.release()
			return
		if action == "get info":
			lock.acquire()
			response = get_info(username, password)
			confd.send(response.encode('utf-8'))
			confd.close()
			logging(response)
			lock.release()
			return
		if action == "refund":
			bill_id = request.get("bill id")
			lock.acquire()
			response = refund(username, password, bill_id)
			confd.send(response.encode('utf-8'))
			confd.close()
			logging(response)
			lock.release()
			return
		lock.acquire()
		confd.send(error("fail").encode())
		lock.release()
	except socket.error as err: 
		print(err)
def start():
	try:
		confd = socket.socket()
	except socket.error: 
		print('error create socket')
	confd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)	
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