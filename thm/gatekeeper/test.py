#!/usr/bin/env python3

import socket, sys

host = "10.10.128.185"
port = 31337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(bytes("shit" + "\r\n", 'latin-1'))
print(str(s.recv(1024), 'utf-8'))
print("Crashed :)")