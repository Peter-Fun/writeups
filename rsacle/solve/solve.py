# jayden was here
from pwn import *
from z3 import *
from sympy.ntheory.modular import crt
import gmpy2
from z3mt import mt_gen_sol, timeit, N
from itertools import islice
from tqdm import tqdm
from sage.all import PolynomialRing, ZZ, Zmod
from Crypto.Util.number import long_to_bytes


io = process(["python3", "../chall.py"])
# io = remote("localhost", 1337)

io.recvuntil(b"Length of flag: ")
flag_length = int(io.recvline().strip())

sol = Solver()

state = [BitVec(f"state_{i}", 32) for i in range(N)]
stategen = islice(mt_gen_sol(sol, state), 32, None)

ms = []

for i in tqdm(range(64)):
    io.sendline(b"1")

    c = []
    m = []

    for _ in range(3):
        ci, _e, ni = map(int, io.recvline().decode().strip().split())
        c.append(ci)
        m.append(ni)

    idk, _ = crt(m, c)

    random_bits = int(gmpy2.iroot(idk, 3)[0])

    ms.extend(m)
    for _ in range(32):
        s1 = random_bits & 0xFFFFFFFF
        sol.add(s1 == next(stategen))
        random_bits >>= 32

with timeit("z3 solving"):
    assert sol.check() == sat

m = sol.model()

state = [m.evaluate(s).as_long() for s in state]

rand = random.Random()
rand.setstate((3, tuple(state + [624]), None))

padding = rand.getrandbits(1024)

io.sendline(b"2")
enc_flag, e, n = map(int, io.recvline().decode().strip().split())

rand.getrandbits(1024 * 64)

n = ms[rand.randint(0, 2)]

io.close()

R = PolynomialRing(Zmod(n), 'x')
x = R.gen()

shift = 8 * (flag_length - 1) + 7

padded_flag = padding * (2**shift) + x
f = padded_flag**e - enc_flag

roots = f.small_roots(X=2**(flag_length*8))


flag = long_to_bytes(ZZ(roots[0]))
if flag.startswith(b'FFCTF{') and flag.endswith(b'}'):
    print(f"flag: {flag.decode('utf-8')}")
