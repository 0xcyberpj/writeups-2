# Hardening Basics Part 1


## SUDO

- Stands for `Super User Doer`
- Allows non root user to run the applation as root

```bash
# obtain the groups which the current user is a memnber of
groups

# add a user to a certian groups
usermod -aG {group name} {user name}

# obtian the permissions that the users can run as SUDO
sudo -l

# grant a user all to execute all application as root without password
{username} ALL=(ALL:ALL) ALL NOPASSWD: ALL

# disable root ssh login
 - change "PermitRootLogin" to "no"

# to avoid privesc using the text editors like vim, implement sudoedit
# in the sudoers file
{username} ALL=(ALL) sudoedit {filename}

# the requirements for password (password complexity) can be assigned with the help of pwquality pam module and configuring the pwquality.conf file in /etc/security
# install pwquality pam module
sudo apt-get install libpam-pwquality
# the default configuration can be found in /etc/pam.d/common-password
# this file specifies the no. of retries that can be done on event of wrong password
cat /etc/pam.d/common-password | grep pwquality
# in the /etc/security/pwquality.conf file we can specify the password complexity for the users

# password expiration can be configured within the "Password Aging Control" Section of /etc/login.defs
# Password aging controls:                                                                                      
#                        
#       PASS_MAX_DAYS   Maximum number of days a password may be used.
#       PASS_MIN_DAYS   Minimum number of days allowed between password changes.
#       PASS_WARN_AGE   Number of days warning given before a password expires.
#                                                                                                                                                     
PASS_MAX_DAYS   99999        
PASS_MIN_DAYS   0        
PASS_WARN_AGE  7
```

## Chapter 1 QUIZ

-  What group are users automatically added to in Ubuntu?
`sudo`

- What would be the command to add an existing user, nick, to the sudo group? You're running as root
`usermod -aG sudo nick`

- What command as a user can we enter to see what we are allowed to execute with sudo?
`sudo -l`

- Where is the sudo policy file stored?
`/etc/sudoers`

- When in visudo and you see %____, what does the % sign indicate that you are dealing with?
`group`

- This Alias lets the user assign a name, like "ADMINS" to a group of people
`user`

- Which Alias allows you to create a set of commands that you can then assign to a User Alias?
`command`

- Yey/Ney - emacs has a shell escape
`Yey`

- What is the minimum recommended password length set by NIST?
`8`

- When using the pwhistory module, which file will contain the previous passwords for the user?
`opasswd`

- What principle states that every user only has enough access to do their daily duties and tasks
`principle of least privilege`
