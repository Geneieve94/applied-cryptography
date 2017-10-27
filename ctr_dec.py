#!/usr/bin/python2
import binascii
from binascii import *
from Crypto.Cipher import AES
from Crypto import Random
from multiprocessing import *
import string
import sys



def Xoring(a,b):
    print a
    print b
    c=int(a,16)^int(b,16)
    c=format(c,'#034x')[2:]
    return c

def ECBencrypt(key, raw):
    if (raw is None) or (len(raw) == 0):
        raise ValueError('input text cannot be null or empty set')
    cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
    ciphertext = cipher.encrypt(raw)
    return binascii.hexlify(bytearray(ciphertext)).decode('utf-8')

def ctr_enc(key,IV_ctr,enc):
    init_i= ECBencrypt(key,unhexlify(IV_ctr))
    pi = Xoring(init_i,enc)
    #print pi
    pi=unhexlify(pi)
    return pi

def ctr_enc_helper(x):
    return ctr_enc(x[0],x[1],x[2])



if   __name__ == "__main__":
    #print sys.argv
    BS = 32
    f_key = open(sys.argv[(sys.argv.index("-k") + 1)], 'r')
    KEY = f_key.read()
    # f_iv = open(sys.argv[(sys.argv.index("-v") + 1)],'r')
    # iv = f_iv.read()
    f_enc=open(sys.argv[(sys.argv.index("-i") + 1)],'r')
    enc = f_enc.read()
    iv = enc[:32]
    enc = enc[32:]
    if len(enc) % 16 == 0:
        nb = len(enc) / BS
    else:
        nb=len(enc)/BS+1
    print nb
    arg_list=[[0,0,0]]
    for i in range(0,nb-1):
        arg_list.append([0,0,0])
    for i in range (0,nb):
        arg_list[i][0]=KEY
        arg_list[i][1] = format(int(iv, 16) + 1,'#034x')[2:]
        arg_list[i][2]= enc[BS*i:BS*(i+1)]

    print arg_list

    p= Pool(4)
    pi =p.map(ctr_enc_helper,arg_list)
    print pi
    pt=''
    for i in range (0,nb):
       pt=pt+pi[i]
    print pt
    text = open(sys.argv[(sys.argv.index("-o") + 1)], "wb+")
    text.write(pt)
    text.close()











