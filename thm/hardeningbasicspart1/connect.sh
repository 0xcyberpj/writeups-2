#!/usr/bin/bash

ssh-keyscan -H $1 >> ~/.ssh/known_hosts
sshpass -p 'tryhackme' ssh spooky@$1
