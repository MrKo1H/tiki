import sys
import json
import Request

def sign_in(username, password):
	request = json.dumps({"action":"sign in", "username":username, "password":password}).encode('utf-8')
	response = json.loads(Request.request(msg=request).decode('utf-8'))
	return response

def use_tool(username, password, tool_name):
	request = json.dumps({"action":"use tool", "username":username, "password":password, "tool name":tool_name}).encode("utf-8")
	response = json.loads(Request.request(msg=request).decode('utf-8'))
	return response

def sign_up(username, password):
	request = json.dumps({"action":"sign up", "username":username, "password":password}).encode('utf-8')
	response = json.loads(Request.request(msg=request).decode('utf-8'))
	return response

def get_info(username, password):
	request = json.dumps({"action":"get info", "username":username, "password":password}).encode('utf-8')
	response = json.loads(Request.request(msg=request).decode("utf-8"))
	return response

def log(username, password, bill_id, tool_name):
	request = json.dumps({"action":"log", "username":username, "password":password, "bill id":bill_id}).encode('utf-8')
	response = json.loads(Request.request(msg=request).decode('utf-8'))
	return response

print(sign_in("addd", "abcD1234"))
print(get_info("bbb", "abcD1234"))
