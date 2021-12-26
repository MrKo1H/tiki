import socket
import sys
import json

IP 			="18.117.174.245"
#IP = "127.0.0.1"
PORT = 8888
BUFFER_SIZE = 1024
auth_token = ""

def sign_in(username, password):
	s = socket.socket()
	s.connect((IP,PORT))
	request = json.dumps({"action":"sign in", "username":username, "password":password}).encode('utf-8')
	s.send(request)
	response = json.loads(s.recv(BUFFER_SIZE).decode('utf-8'))
	global auth_token
	auth_token = response["auth_token"]
	print(response)

def use_tool(tool):
	global auth_token
	s = socket.socket()
	s.connect((IP,PORT))
	request = json.dumps({"action":"use tool", "auth_token":auth_token, "tool":tool}).encode("utf-8")
	s.send(request)
	response = json.loads(s.recv(BUFFER_SIZE).decode("utf-8"))
	auth_token = response.get("auth_token")
	print(response)

def sign_up(username, password):
	s = socket.socket()
	s.connect((IP,PORT))
	request = json.dumps({"action":"sign up", "username":username, "password":password}).encode('utf-8')
	s.send(request)
	reponse = json.loads(s.recv(BUFFER_SIZE).decode('utf-8'))
	print(response)
def log_out(username):
	pass

