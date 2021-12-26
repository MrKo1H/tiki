import socket
import sys
import json

IP 			="18.117.174.245"
IP  		="127.0.0.1"
PORT 		= 8888
BUFFER_SIZE = 1024

## request to server msg and get response
def request(msg):
	s = socket.socket()
	s.connect((IP, PORT))
	s.send(msg)
	return s.recv(BUFFER_SIZE)
