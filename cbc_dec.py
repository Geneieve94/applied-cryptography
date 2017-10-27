#!/usr/bin/python2
import binascii
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto import Random
import sys



def unpadding(rawplaintext):
    listofplaintextblock = []
    flag = 0
    while flag + 16 <= len(rawplaintext):
        listofplaintextblock.append(rawplaintext[flag:flag+16])
        flag += 16


    plaintext = ""
    # print listofplaintextblock[-1]
    if listofplaintextblock[-1] == "10101010101010101010101010101010".decode("hex"):
        for block in listofplaintextblock[:-1]:
            plaintext += block
        return plaintext
    else:
        numberofpadding = int(listofplaintextblock[-1][-1].encode("hex"), 16)
        lastblock = listofplaintextblock[-1][:16-numberofpadding]
        for block in listofplaintextblock[:-1]:
            plaintext += block
        return plaintext + lastblock

def Xoring(a,b):
    c=int(a,16)^int(b,16)
    c=format(c,'#034x')[2:]
    return c

def ECBdecrypt(key, enc):
    if (enc is None) or (len(enc) == 0):
        raise ValueError('input text cannot be null or empty set')
    enc = binascii.unhexlify(enc)
    cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
    enc = cipher.decrypt(enc)
    return enc

def CBCdecrypt(IV,cipher,key,BS):
    pt = ''
    for i in range (0,len(cipher)/BS):
        cipher_b = cipher[BS*i:BS*(i+1)]
        ci = ECBdecrypt(key,cipher_b)
        cih=binascii.hexlify(ci)
        pti= Xoring(cih,IV)
        pt = pt+unhexlify(pti)
        IV = cipher_b

    return pt


if __name__ == "__main__":
    #print sys.argv
    f_key = open(sys.argv[(sys.argv.index("-k") + 1)], 'r')
    KEY = f_key.read()
    f_cipher = open(sys.argv[(sys.argv.index("-i") + 1)], 'r')
    cipher = f_cipher.read()
    BS = 32
    f_IV = open(sys.argv[(sys.argv.index("-v") + 1)],'r')
    IV = f_IV.read()
    plaint = CBCdecrypt(IV, cipher, KEY, BS)

    ooo = open(sys.argv[(sys.argv.index("-o") + 1)], "wb+")
    ooo.write(unpadding(plaint))
    ooo.close()
    # print plaint
