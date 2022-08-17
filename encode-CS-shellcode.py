#!/usr/bin/python

import argparse
import pyscrypt
from os import urandom
import os
from textwrap import wrap


# XOR Functions

#------------------------------------------------------------------------

def xor(data, key):
    l = len(key)
    keyAsInt = map(ord, key)
    return bytes(bytearray((
        (data[i] ^ keyAsInt[i % l]) for i in range(0,len(data))
    )))


# Output Formating



def formatCPP(data, key):

    shellcode = "\\x"

    shellcode += "\\x".join(format(ord(b),'02x') for b in data)
    print('char key[] = "' + key +'";')
    print("char encryptedShellcode[] = \n")
    n = 64
    chunks = [shellcode[i:i+n] for i in range(0, len(shellcode), n)]
    last_elem = chunks.pop()
    for i in chunks:
        print('    "'+i+'"')


    print('    "'+last_elem+'"'+";")



# Main Function

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("shellcodeFile", help="File name containing the raw shellcode to be encoded/encrypted")
    parser.add_argument("key", help="Key used to transform (XOR or AES encryption) the shellcode")
    args = parser.parse_args() 



    # Open shellcode file and read all bytes from it

    try:

        with open(args.shellcodeFile) as shellcodeFileHandle:
            shellcodeBytes = bytearray(shellcodeFileHandle.read())
            shellcodeFileHandle.close()

    except IOError:
        quit()


    # Display formated output
    masterKey = args.key
    transformedShellcode = xor(shellcodeBytes, masterKey)
    formatCPP(transformedShellcode, masterKey)

quit()
