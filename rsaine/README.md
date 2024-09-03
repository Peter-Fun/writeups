# RSAcle Writeup
## Description
The Great RSAcle has spoken. The five wishes have been granted. The rest is up to you.

## Solution
Upon inspection, we can see that the challenge encrypts a 1024 bit padded flag message using RSA with `e = 5` and five different values of n. 

This is an example of Håstad's broadcast attack, which involves the same message being encrypted with different modulos in RSA being recovered without ever having to figure out what the decryption key is. This is all possible due to the small public exponent of 5 being coupled with 5 encryptions.

Assuming that all of the modulos are relatively prime, we can use the Chinese Remainder Theorem to compute C such that C mod every value of n is equal to the corresponding ciphertexts.

Since this means that C is equal to the padded flag ^ 5 mod the product of all values of n, and that the padded flag ^ 5 has to be less than the product of all values of n, C is equal to padded flag ^ 5, meaning that if we take the fifth root of C, we can get the padded flag and retrieve the actual flag!

To implement the Chinese Remainder Theorem, the gmpy2 module was included to make inverse easier.

The program gives us an output of ```b'\xf9\x07\x9f\x10\xa6(b\xcbI\x1f\xf7\xe5\xa5pN\x89w0\x95Rj\x9f\xe8S\x8b\xb1\x9eq(&\x0c\x07\x04Q3\x94\x8d\x05\x1b<\xd0\x84\xa2\x7f\x00%65\x1b\xcb\x04\x9f\xcd;*\xf0\x1e\xef\xbbN\x9a\x04 a\x84.\xc3(\x00\x8dD\xb2\xfd\xd8\x1e\xb7\xc7$\x19\x04\x8el@\xcf2a\x8a\x1dt\xc5\x86\xb4\xb8V\xeb\x02\x1b\xa8\x04\xa8\xf4\xee\x01\x8c\xd4\xa9\x0b\x19\x1e\xd9\xb8e\xcf\x9b\xf8\xd0}a\xaf\x1c_\xe8)\x7f\xaa\xd9\x9d\xe2FFCTF{1tz_4_m1r4cl3}'```

`FFCTF{1tz_4_m1r4cl3}`


