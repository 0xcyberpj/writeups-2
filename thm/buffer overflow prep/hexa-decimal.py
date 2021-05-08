#!/usr/bin/env python3

for i in range(1, 256):
    print("\\x" + "{:02x}".format(i), end="")
    
print()
