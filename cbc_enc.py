#!/usr/bin/python2
import binascii
from Crypto.Cipher import AES
from binascii import *
from Crypto import Random
import sys

#padding generation



def padding(inputfile):
    # inputdata = open(inputfile)
    textblock = []
    flag = 0
    index = 0
    while index < len(inputfile):
        if index + 16 > len(inputfile):
            textblock.append(inputfile[index:])
            flag = 1
            break
        if index + 16 == len(inputfile):
            textblock.append(inputfile[index:])
            break
        # print inputfile[index:16]
        textblock.append(inputfile[index: index + 16])
        index += 16

    if flag == 1:
        numtopad = 16 - len(textblock[-1])
        lastblock = textblock[-1]
        padding = ""
        for _ in xrange(numtopad):
            padding += str("0"+hex(numtopad)[-1])
        lastblock += padding.decode("hex")
        textblock[-1] = lastblock
    else:
        lastblock = "10101010101010101010101010101010".decode("hex")
        textblock.append(lastblock)

    paddedstring = ""
    for block in textblock:
        paddedstring += block
    return paddedstring

def Xoring(a,b):
    c=int(a,16)^int(b,16)
    c=format(c, '#034x')[2:]
    return c

def ECBencrypt(key, raw):
    if (raw is None) or (len(raw) == 0):
        raise ValueError('input text cannot be null or empty set')
    cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
    ciphertext = cipher.encrypt(raw)
    return binascii.hexlify(bytearray(ciphertext)).decode('utf-8')



def CBC_ENC(inputF,IV,k,BS):
    ct=''
    msg_pad = padding(inputF)
    for i in range(0,len(msg_pad)/BS):
        msg_blocksize=hexlify(msg_pad[BS*i:BS*(i+1)])
        d=unhexlify(Xoring(msg_blocksize,IV))
        ci=ECBencrypt(k,d)
        ct= ct+ci
        IV=ci
    return ct

if __name__ == "__main__":
    #print sys.argv
    f_key= open(sys.argv[(sys.argv.index("-k") + 1)],'r')
    KEY=f_key.read()
    f_input = open(sys.argv[(sys.argv.index("-i") + 1)], 'r' )
    inputFile=f_input.read()
    f_IV = open(sys.argv[(sys.argv.index("-v") + 1)],'r')
    IV = f_IV.read()
    print IV
    BS = AES.block_size
    cipher=CBC_ENC(inputFile,IV,KEY,BS)
    print cipher
    f_cipher= open(sys.argv[(sys.argv.index("-o") + 1)],'wb')
    f_cipher.write(cipher)
    f_cipher.close()