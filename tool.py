import sqlite3


TOOL_FILE_DB	= "tool.db"
TABLE 			= "tools"
TOOL_CONNECTION = sqlite3.connect(TOOL_FILE_DB, check_same_thread=False)
TOOL_CURSOR     = TOOL_CONNECTION.cursor()
TOOL_FILE_LOAD  = "list_tools.txt"

def make_models():
	global TOOL_CONNECTION, TOOL_CURSOR, TABLE
	TOOL_CURSOR.execute(f"DROP TABLE IF EXISTS {TABLE};")
	TOOL_CURSOR.execute(f"""CREATE TABLE {TABLE}(
		name varchar(100),
		cost BIGINT
		);""")
	TOOL_CONNECTION.commit()


def add_tool(tool, cost):
	global TOOL_CONNECTION, TOOL_CURSOR, TABLE
	TOOL_CURSOR.execute(f'INSERT INTO {TABLE} (name, cost) VALUES ("{tool}",{cost});')
	TOOL_CONNECTION.commit()

def change_cost(tool, cost):
	global TOOL_CONNECTION, TOOL_CURSOR, TABLE
	TOOL_CONNECTION.execute(f'UPDATE TABLE SET cost={cost} WHERE name="{tool}";')
	TOOL_CONNECTION.commit()

def get_cost(tool):
	global TOOL_CURSOR, TABLE
	TOOL_CURSOR.execute(f'SELECT cost FROM {TABLE} where name="{tool}"')
	x = TOOL_CURSOR.fetchall()
	return x[0][0]

def import_from_file(file):
	try:
		f = open(file, "r")
		l = f.read().split("\n")
		for x in l:
			xx = x.split(" ")
			add_tool(xx[0], int(xx[1]))
	except Exception as e:
		print(e)
		return

