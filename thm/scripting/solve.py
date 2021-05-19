from base64 import *

def d_b64(temp):
	temp2 = b64decode(temp)
	print("Decoded Value: ", str(temp[0:15], 'utf-8'))

	try:
		d_b64(temp)
	except Exception as e:
		print(e)

with open('task.txt', 'r') as f:
	data = f.readline()
	data = bytes(data,'utf-8')

temp = b64decode(data)
d_b64(temp)

"""
line 13: opening the file in read mode
line 14: reading each line in the file
line 15: encoding the read line and storing in a variable named data

line 17: since we know its a b64 encoded file, decode it for the first time and store the output in temp variable
line 18: calling the created d_b64() passing the decoded base64 Value

line 3: creating a custom function for decoding
line 4: decoding the obtained input and storing in a variable temp2
line 5: slicing the first 14 characters from the output of temp2
line 7: try except block
line 8: the funciton is called, now the previously decoded value is passed to the function, which is still a base64 value
and will be decoded again and again until the padding for syntax errors out
Print characters from 0 - 14 from each decoded value, to obtain flag


much easier code by WireInTheGhost
import base64

with open('task.txt', 'r') as f:
	data = f.readline()

for _ in range(50):
	data = b64decode(data)

print(data)
"""
