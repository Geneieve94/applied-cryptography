# applied-cryptography
homework1 for applied cryptography
 
This repo include four artifacts which are cbc_enc.py, cbc_dec.py, ctr_enc.py, ctr_enc.py.
These four executable files do the work that encrypt and decrypt files with CBC and CTR mode.

The 'inputfile' is my plaintext file for the executable file, the 'key' is also mine, the outPutFile_cbc and outPutFile_ctr are the encryption files of ctr and cbc mode.
The 'IV' is the Initial vector for the two mode. 
The keyFile 1,2 and testFile1,2,3 are sample given from professor.

To execute the source code, a user should type command into terminal as shown below:

python codefilename -i inputfile -o outputfile -k keyfile -v IV file

The text_cbc and text_ctr are the output testfile from cbc_dec and ctr_dec, these two files are come from testFile1 and keyfile1.

