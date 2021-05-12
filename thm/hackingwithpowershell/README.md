# Hacking with Powershell

- Basics
  - Syntax for commandlets: `Verb-Noun`
  - Top Verbs: `Get, Start, Stop, Read, Write, New, Out`

| Command | Summary |
|---------|---------|
| `Get-Help {command-name}` | Displays information on how to use a command |
| `Get-Help {command-name} -examples` | Displays help with examples|
| `Get-Command` | Gets all the commands installed on the computer| 
| `Get-Command New-*` | Displays all the commands with the New Verb |
| `Get-ChildItem` | Displays the contents of the current folder |
| `Get-ChildItem | Select-Object -Property mode, name` | Displays just the File permission and name in the current folder |
| `Where-Object -Property {propertyName} -operator(contains,eq,gt) {value}` | Filters the output to match a very specific value |
| `Sort-Object` | sorts in ascending order |
| `Get-ChildItem -Path C:/ -include *.{filename.ext | .ext}* -Recurse -ErrorAction SilentlyContinue` | Locate a file with the filename / extension |
| `measure` | Lists the total no of line | 
| `Invoke-WebReques` | Makes Web Requests | 
| `Certutil` | Utiltity to make webrequest, encode & decode base64 |


## Answers 

```powershell
# obtain parameters of a command (arguments passed to the command with "-{paramName}")
(Get-Command Get-FileHash).Parameters

# Get the displayed by the specific cmdlet (output by the commandlet)
Get-LocalUser | Get-Member

# Manual pages
get-help

# locating a file
Get-ChildItem -Path C:\ -Recurse -Include *intresting-file.txt* -ErrorAction SilentlyContinue

# Contents of a file
Get-Contents C:\Program Files\intresting-file.txt.txt

# Count no of lines form the output of get-commands
Get-Commands | measures

# Count only the Object type of cmdlets
Get-Commands | where commandtype -eq cmdlet | measure

# obtain hash for a file in specific algorithm
Get-FileHash -Path "C:\Program Files\intresting-file.txt.txt" -Algorithm md5

# Make a webrequest
Invoke-WebRequest -uri 'https://cyberwr3nch.github.io' -outfile 'index.html'

# base64 encode a file with certutil 
certutil -encode inputFile outputFile

# base64 decode  a file with certutil
certutil -decode base64_encodedFile outputFile

# web request with certutil
certutil -urlcache -f 'https://cyberwr3nch.github.io' index.html

# Enumerate users
Get-LocalUsers

# Get users on specific attribute
Get-LocalUsers | where sid -eq S-1-5-21-1394777289-3961777894-1791813945-501

# IP Address information
Get-NetIPAddress

# obtain listening ports
Get-NetTCPConnection

# obtain patch information
Get-HotFix

# Search for all files containg a specific string
Get-ChildItem C:\* -Recurse | Select-String -pattern API_KEY

# Get running process
Get-Process

# Obtain ownership inforamtion
Get-ACL {path}
```