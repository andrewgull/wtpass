#!/usr/bin/python3

from cryptography.fernet import Fernet
import json
import argparse
import subprocess
import sys

# set files' paths
# use encryptor.py to generate %filename_key
passes_en = "example_passes_encrypted"
key_en = "example_passes_key"

def encrypt(f_obj, keyy):
    """
    reads raw text file object and encrypts it using pre-generated key
    :param f_obj: raw text file object
    :param keyy: encryption key
    :return: encrypted object
    """
    # f = open(file, 'rb').readline()
    k = open(keyy, 'rb').readline()
    cipher_suite = Fernet(k)
    encrypted = cipher_suite.encrypt(str(f_obj).encode())
    return encrypted


def decrypt(file, keyy):
    """
    reads encrypted file and decrypts it
    :param file: encrypted file
    :param keyy: encryption key
    :return: decrypted file as text (bytes)
    """
    f = open(file, 'rb').readline()
    k = open(keyy, 'rb').readline()
    cipher_suite = Fernet(k)
    decrypted = cipher_suite.decrypt(f)
    return decrypted

def first_encryptor(file):
    k = Fernet.generate_key()
    f = open(file, 'rb').readline()
    # k = open(keyy, 'rb').readline()
    cipher_machine = Fernet(k)
    encrypted = cipher_machine.encrypt(f)
    with open(file + "_key", 'wb') as out:
        out.write(k)
    print("Key generated.\nKeep the key in a safe place!")
    with open(file + "_encrypted", "wb") as out:
        out.write(encrypted)
    print("file %s have been encrypted" % file)

def read_decrypt():
    # read and decrypt passes file
    passes_de = decrypt(passes_en, key_en)
    passes = json.loads(passes_de.decode())
    return passes

# make argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--first", action="store_true", help="use for initial encryption of your file")
parser.add_argument("pass_record", nargs="?", default=None, help="display log and key")
parser.add_argument("-k", "--keys", action="store_true", help="display all existing keys")
parser.add_argument("-a", "--add", action="store_true", help="add new pass record")
parser.add_argument("-d", "--delete", action="store_true", help="delete an existing pass record")
parser.add_argument("-g", "--generate", action="store_true", help="generate new password with openssl")
parser.add_argument("-c", "--change", action="store_true", help="change existing record")
parser.add_argument("-dc", "--decrypt", action="store_true", help="decrypt your file for some reasons")
args = parser.parse_args()

# encrypt for the first time
if args.first:
    filepath = input("enter file path > ")
    first_encryptor(filepath)

# decrypt file
elif args.decrypt:
    filepath = input("enter file path > ")
    keypath = input("enter key path > ")
    decrypted = decrypt(filepath, keypath)
    with open("your_decrypted_file", 'wb') as out:
        out.write(decrypted)
    print("your file have been decrypted")

# print all keys
elif args.keys:
    passes_jsn = read_decrypt()
    for key in passes_jsn["data"]:
        print(key)

# generate a new pass by openssl
elif args.generate:
    print("I generated this pass:")
    print(subprocess.call(["openssl", "rand", "-base64", "12"]))

# add new pass record
elif args.add:
    passes_jsn = read_decrypt()
    new_key = input("enter new key > ")
    new_pass = input("enter new pass > ")
    new_log = input("enter new log > ")
    pass_record = {'pass': new_pass, 'log': new_log}
    passes_jsn['data'][new_key] = pass_record
    # make string from dict
    passes_str = json.dumps(passes_jsn)
    # encrypt passes (as string, not JSON!) again with already existing key
    passes_str_en = encrypt(passes_str, key_en)

    with open(passes_en, 'wb') as outfile:
        outfile.write(passes_str_en)
    print("new item added")

elif args.delete:
    passes_jsn = read_decrypt()
    # delete item
    key = input("enter key to remove > ")
    try:
        del passes_jsn['data'][key]
    except KeyError:
        print("this keyword doesn't exist")
        sys.exit()
    passes_str = json.dumps(passes_jsn)
    passes_str_en = encrypt(passes_str, key_en)
    with open(passes_en, 'wb') as outfile:
        outfile.write(passes_str_en)
    print("key %s deleted" % key)

elif args.change:
    passes_jsn = read_decrypt()
    key = input("enter key to change > ")
    new_pass = input("enter new pass > ")
    new_log = input("enter new log > ")
    log_pass = {'pass': new_pass, 'log': new_log}

    try:
        passes_jsn['data'][key] = log_pass
    except KeyError:
        print("this keyword doesn't exist")
        sys.exit()
    passes_str = json.dumps(passes_jsn)
    passes_str_en = encrypt(passes_str, key_en)
    with open(passes_en, 'wb') as outfile:
        outfile.write(passes_str_en)
    print("key %s have been changed" % key)

elif args.pass_record:
    passes_jsn = read_decrypt()
    try:
        ans_pass = passes_jsn['data'][sys.argv[1]]['pass']
    except KeyError:
        print("this keyword doesn't exist")
        sys.exit(1)
    # and continue if key is OK
    ans_log = passes_jsn['data'][sys.argv[1]]['log']
    print("log: %s\npass: %s" %(ans_log, ans_pass))
