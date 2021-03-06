#!/usr/bin/python2
import binascii
from binascii import *
from Crypto.Cipher import AES
from multiprocessing import Pool
import sys
import os

def Xoring(a,b):
    c=int(a,16)^int(b,16)
    c = format(c, '#034x')[2:]
    return c

def ECBencrypt(key, raw):
    if (raw is None) or (len(raw) == 0):
        raise ValueError('input text cannot be null or empty set')
    cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
    ciphertext = cipher.encrypt(raw)
    return binascii.hexlify(bytearray(ciphertext)).decode('utf-8')


def ctr_enc(key,IV_ctr,msg):
    init_i= ECBencrypt(key,unhexlify(IV_ctr))
    ci = Xoring(init_i,hexlify(msg))
    # NUM += 1
    # print arg_list.index( [key, IV_ctr, msg] ), ci
    return ci


def ctr_enc_helper(x):
    return ctr_enc(x[0],x[1],x[2])



if __name__ == "__main__":
    #print sys.argv
    BS = 16
    f_key = open(sys.argv[(sys.argv.index("-k") + 1)], 'r')
    KEY = f_key.read()
    if "iv" in sys.argv:
        f_iv = open(sys.argv[(sys.argv.index("-v") + 1)],'r')
        iv = f_iv.read()
    else:
        iv = os.urandom(16).encode("hex")
    f_msg=open(sys.argv[(sys.argv.index("-i") + 1)],'r')
    msg = f_msg.read()
    print len(msg) / 16
    if len(msg) % 16 == 0:
        nb = len(msg) / BS
    else:
        nb=len(msg)/BS+1
    arg_list=[]

    for i in range(nb):
        arg_list.append([0,0,0])

    for i in range (nb):
        arg_list[i][0]=KEY
        arg_list[i][1] = format(int(iv, 16) + 1,'#034x')[2:]
        arg_list[i][2]= msg[BS*i:BS*(i+1)]

    print arg_list
    print len(arg_list)

    p= Pool(4)
    ci =p.map(ctr_enc_helper,arg_list)
    # print "afsda"
    ct=''
    for i in range (0,nb):
       ct=ct+ci[i]
    ct = iv + ct
    f_cipher = open(sys.argv[(sys.argv.index("-o") + 1)], 'wb')
    f_cipher.write(ct)
    f_cipher.close()




