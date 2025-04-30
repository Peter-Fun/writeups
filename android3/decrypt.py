finalbytes = [3, 92, 7, 83, 104, 73, 80, 4, 83, 0, 1, 7, 2, 80, 2, 82, 1, 81, 5, 3, 84, 85, 83, 83, 94, 13, 3, 4, 82, 6, 93, 85, 7, 0, 81, 87, 86, 5, 78]
vals = "e0f472325bc64f479b13a121895ed39d"
bytes = [ord(i) for i in vals]

password = []
for i in range(len(finalbytes)):
    password.append(chr(finalbytes[i] ^ bytes[i % len(bytes)]))
print("".join(password))