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


data = """0564408103 abcD1234
0564408221 abcD1234
0564408227 abcD1234
0564408010 abcD1234
0564408158 abcD1234
0564408141 abcD1234
0564408224 abcD1234
0582749657 ABcd1234
0582792955 ABcd1234
0582794490 ABcd1234
0582792943 ABcd1234
0582795037 ABcd1234
0582794604 ABcd1234
0582738845 ABcd1234
0582792947 ABcd1234
0582748310 ABcd1234
0582792949 ABcd1234""".split("\n")
create_table()
for x in data:
	xx = x.split(" ")
	add_user(xx[0], xx[1], 1000)
