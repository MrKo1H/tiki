import sys
import json
import Request

def sign_in(username, password):
	request = json.dumps({"action":"sign in", "username":username, "password":password}).encode('utf-8')
	response = Request.request(msg=request)
	print(response)

def use_tool(username, password, tool):
	request = json.dumps({"action":"use tool", "username":username, "password":password, "tool":tool}).encode("utf-8")
	response = Request.request(msg=request)
	print(response)

def sign_up(username, password):
	request = json.dumps("action":"sign up", "username":username, "password":password)
	response = Request.request(msg=request)
	print(response)
	
def get_info(username, password):
	request = json.dumps("action":"get info", "username":username, "password":password)
	response = Request.request(msg=request)
	print(response)