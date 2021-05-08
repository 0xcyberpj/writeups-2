#!/usr/bin/env python3

import socket, sys

host = "127.0.0.1"
port = 31337
payload = "a"*100
timeout=2

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(s.recv(1024))
            s.send(bytes("aaaa", 'latin-1'))
            print(s.recv(1024))
    except:
        print("Conenction error")
        sys.exit(0)
