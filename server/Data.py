import sqlite3
import json


FILE   		= "data.db"
CONNECTION	= sqlite3.connect(FILE, check_same_thread=False)
CURSOR  	= CONNECTION.cursor()
TABLE_NAME	= "users"

def create_table():
	global CURSOR, CONNECTION
	CURSOR.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
	CURSOR.execute(f"""CREATE TABLE {TABLE_NAME}(
		username varchar(30) PRIMARY KEY,
		password varchar(30),
		credit BIGINT
	);""")
	CONNECTION.commit()
def check_user(username, password):
	global CURSOR
	CURSOR.execute(f'SELECT username FROM {TABLE_NAME} WHERE username="{username}" AND password="{password}";')
	l = CURSOR.fetchall()
	if not l:
		return False
	return True

def get_info(username, password):
	global CURSOR
	CURSOR.execute(f'SELECT username, password, credit FROM {TABLE_NAME} WHERE username="{username}" AND password="{password}";')
	l = CURSOR.fetchall()[0]
	return json.dumps({"username":l[0], "password":l[1], "credit":l[2]})
def add_user(username, password,credit = 0):
	global CURSOR
	CURSOR.execute(f'INSERT INTO {TABLE_NAME} VALUES("{username}", "{password}", {credit})')
	CONNECTION.commit()
def get_credit(username,password):
	global CURSOR
	CURSOR.execute(f'SELECT credit FROM {TABLE_NAME} WHERE username="{username}" and password="{password}";')
	x = CURSOR.fetchall()[0]
	return x[0]

def sub_credit(username, password, amount):
	global CURSOR, CONNECTION
	x = get_credit(username, password)
	CURSOR.execute(f'UPDATE {TABLE_NAME} SET credit={x - amount};')
	CONNECTION.commit()
	
def set_credit(username, password, value):
	global CURSOR, CONNECTION
	CURSOR.execute(f'UPDATE {TABLE_NAME} SET credit="{value}";')
	CONNECTION.commit()

