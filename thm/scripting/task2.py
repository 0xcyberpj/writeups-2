from bs4 import BeautifulSoup
from pwn import *
import requests
import socket
import sys
import re

# variable
#val = 0


def ident_port():
    #print(" make a connection to the machine on port 3010 to findout which port is alive")
    s = requests.get(url="http://10.10.86.2:3010")
    if s.status_code == 200:
    	log.success("Successfully connected to source webpage")
    	html = BeautifulSoup(s.text, 'html.parser')
    	port = html.findAll('a')[0].text
    	print(f"Found port: {port}")
    	conn2(port)


def comp_task(operation, num, n_port):
	val = 0
	num = int(num)
	port = int(n_port)
	log.info(f"The value of val is {val}")
	log.info(f"The recieved operation is {operation}")
	log.info(f"The recieved number is {num}")
	log.info(f"The recieved port is {n_port}")
	

	if operation == "add":
		val += num
		print(val)
	elif operation == 'minus':
		val -= num
		print(val)
	elif operation == 'divide':
		val /= num
		print(val)
	elif operation == 'multiply':
		val *= num
		print(val)
	else:
		print(f"operation invalid: {operation}")

	if port == 9765:
		print("Port 9765 reached stopping script")
		sys.exit(0)
	else:
		conn2(port)


def conn2(port):
	url = f"http://10.10.86.2:{port}"
	print(f"Making 2nd connection to: {url}")
	c = requests.get(url=url)
	if c.status_code == 200:
		print(c.text.split())
		task = c.text.split()
		[operation, num, n_port] = task

		if "STOP" in c.text:
			print(c.text)
		else:
			comp_task(operation, num, n_port)
	else:
		print(c.status_code)




ident_port()