def rsaine():
    from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
    import random
    flag = b"FFCTF{REDACTED}"
    with open("message.txt", "a") as file:
        file.write("I will grant you your five wishes.\n")
        file.write("Length of flag: " + str(len(flag)) + "\n")
        flag = bytes_to_long(flag)
        paddedflag = random.getrandbits(1024) << (len(bin(flag))-1) | flag
        for i in range(1,6):
            file.write("WISH " + str(i) + "\n")
            p = getPrime(1024)
            q = getPrime(1024)
            n = p * q
            file.write(str(pow(paddedflag, 5, n,)) + ", 5, " + str(n) + "\n")
    file.close()

rsaine()