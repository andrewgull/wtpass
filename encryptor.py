#!/usr/bin/python3

from cryptography.fernet import Fernet
import sys


file = sys.argv[1]
mess = open(file).readline()

# code string in byte form: b'string'
mess = mess.encode('utf-8')

key = Fernet.generate_key()
with open(file + "_key", 'wb') as out:
    out.write(key)
print("Key generated")

# use crypting key
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(mess)

# write ciphered text to file
with open(file + "_encrypted", "wb") as out:
    out.write(cipher_text)

print("file %s encrypted" % file)

