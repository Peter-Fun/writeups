#!/usr/local/bin/python
import random
import os
from Crypto.Util.number import getPrime, bytes_to_long

flag = os.environ.get("FLAG", "FFCTF{fake_flag}").encode()

print("Select your option.\n1 - Output a random number encrypted with all our public keys.\n2 - Output the flag, with some added randomness, encrypted with a random public key.")
print("Length of flag:", len(flag))
flag = bytes_to_long(flag)
paddedflag = random.getrandbits(1024) << len(bin(flag)) - 2 | flag

N = []
for i in range(3):
    p = getPrime(1024)
    q = getPrime(1024)
    N.append(p*q)

while True:
    a = input()
    if a == "1":
        c = random.getrandbits(1024)
        for i in N:
            print(pow(c, 3, i), 3, i)

    elif a == "2":
        n1 = N[random.randint(0, 2)]
        n2 = N[random.randint(0, 2)]
        print(pow(paddedflag, 3, n1),
              3, n2)
        break

    else:
        if random.getrandbits(7) == 1:
            print("invald input!")
