from functools import reduce
import gmpy2
import json, binascii


def modinv(a, b):
    return int(gmpy2.invert(gmpy2.mpz(a), gmpy2.mpz(b)))


def chinese_remainder_theorem(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * modinv(p, n_i) * p
    return int(sum % prod)


nset = []
cset = []
with open("message.txt", "r") as file:
    for l in file.readlines():
        if l[0] in "0123456789":
            c,e,n = [int(i.strip()) for i in l.split(",")]
            nset.append(n)
            cset.append(c)
m = chinese_remainder_theorem(nset, cset) # find C using the Chinese Remainder Theorem
m = int(gmpy2.iroot(gmpy2.mpz(m),5)[0]) # find m by taking the fifth root of C

print(binascii.unhexlify(hex(m)[2:]))