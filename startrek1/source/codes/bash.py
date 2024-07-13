from pwn import *
from pwntools import *
galaxies = {} #{2: 2, 1: 1, 7: 7, 9: 9, 11: 11, 14: 14, 15: 15, 16: 16, 5: 15, 3: 3, 6: 6, 19: 41, 46: 46, 12: 12, 52: 23, 4: 75, 18: 18, 80: 80, 76: 41, 43: 43, 51: 51, 8: 8, 83: 83, 85: 85, 91: 91, 81: 62, 64: 64, 70: 91, 94: 94, 77: 77, 65: 65, 10: 10, 17: 17, 79: 79, 84: 84, 87: 87, 44: 82, 47: 30, 21: 3, 31: 8, 88: 67, 35: 96}
# key is galaxy, value is where it goes to
while True:
    p = process("./startrek")
    p.recvuntil(b"(y/n)?")
    p.send(b"n")
    while True:
        try:
            result = p.recvuntil(b"(y/n)?").decode('utf-8')
            landed = int(result[result.index("landed on ") + len("landed on "): result.index("landed on ") + len("landed on ")+3])
            try:
                galaxies[landed] = galaxies[landed]
            except: 
                if "This galaxy contained" in result:
                    new = result[result.index("you were teleported to galaxy ") + len("you were teleported to galaxy "): result.index("you were teleported to galaxy ") + len("you were teleported to galaxy ")+3]
                    galaxies[landed] = int(new)
                else:
                    galaxies[landed] = landed
            p.send(b"n")
        except:
            break
    print(galaxies)
    print(sorted(galaxies.keys()))