from z3 import *
import random
from contextlib import contextmanager
from time import perf_counter

# ------------------
# Start of utility functions
# credits: @y011d4
# ------------------

N = 624
M = 397
MATRIX_A = 0x9908B0DF
UPPER_MASK = 0x80000000
LOWER_MASK = 0x7FFFFFFF


def random_seed(seed):
    init_key = []
    if isinstance(seed, int):
        while seed != 0:
            init_key.append(seed % 2**32)
            seed //= 2**32
    else:
        init_key = seed
    key = init_key if len(init_key) > 0 else [0]
    keyused = len(init_key) if len(init_key) > 0 else 1
    return init_by_array(key, keyused)


def init_by_array(init_key, key_length):
    s = 19650218
    mt = [0] * N
    mt[0] = s
    for mti in range(1, N):
        if isinstance(mt[mti - 1], int):
            mt[mti] = (1812433253 * (mt[mti - 1] ^
                       (mt[mti - 1] >> 30)) + mti) % 2**32
        else:
            mt[mti] = 1812433253 * (mt[mti - 1] ^ LShR(mt[mti - 1], 30)) + mti
    i = 1
    j = 0
    k = N if N > key_length else key_length
    while k > 0:
        if isinstance(mt[i - 1], int):
            mt[i] = (
                (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525)) +
                init_key[j] + j
            ) % 2**32
        else:
            mt[i] = (
                (mt[i] ^ ((mt[i - 1] ^ LShR(mt[i - 1], 30)) * 1664525))
                + init_key[j]
                + j
            )
        i += 1
        j += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1
        if j >= key_length:
            j = 0
        k -= 1
    for k in range(1, N)[::-1]:
        if isinstance(mt[i - 1], int):
            mt[i] = (
                (mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1566083941)) - i
            ) % 2**32
        else:
            mt[i] = (mt[i] ^ ((mt[i - 1] ^ LShR(mt[i - 1], 30)) * 1566083941)) - i
        i += 1
        if i >= N:
            mt[0] = mt[N - 1]
            i = 1
    mt[0] = 0x80000000
    return mt


def update_mt(mt):
    for kk in range(N - M):
        y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
        if isinstance(y, int):
            mt[kk] = mt[kk + M] ^ (y >> 1) ^ (y % 2) * MATRIX_A
        else:
            mt[kk] = mt[kk + M] ^ LShR(y, 1) ^ (y % 2) * MATRIX_A
    for kk in range(N - M, N - 1):
        y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
        if isinstance(y, int):
            mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ (y % 2) * MATRIX_A
        else:
            mt[kk] = mt[kk + (M - N)] ^ LShR(y, 1) ^ (y % 2) * MATRIX_A
    y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK)
    if isinstance(y, int):
        mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ (y % 2) * MATRIX_A
    else:
        mt[N - 1] = mt[M - 1] ^ LShR(y, 1) ^ (y % 2) * MATRIX_A


def temper(state):
    y = state
    if isinstance(y, int):
        y ^= y >> 11
    else:
        y ^= LShR(y, 11)
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    if isinstance(y, int):
        y ^= y >> 18
    else:
        y ^= LShR(y, 18)
    return y


def mt_gen(init_state, *, index=N):
    state = init_state[:]  # copy
    while True:
        index += 1
        if index >= N:
            update_mt(state)
            index = 0
        yield temper(state[index])


def mt_gen_sol(sol, init_state, *, index=N):
    state = init_state[:]  # copy
    twist = 0
    while True:
        index += 1
        if index >= N:
            # replace the new state with new symbolic variables
            # this somehow improve the performance of z3 a lot
            update_mt(state)
            next_state = [BitVec(f"__{twist}_state_{i}", 32) for i in range(N)]
            for x, y in zip(state, next_state):
                sol.add(x == y)
            state = next_state
            twist += 1
            index = 0
        yield temper(state[index])


# ------------------
# Start of testing realted things
# ------------------


@contextmanager
def timeit(task_name):
    print(f"[-] Start - {task_name}")
    start = perf_counter()
    try:
        yield
    finally:
        end = perf_counter()
        print(f"[-] End - {task_name}")
        print(f"[-] Elapsed time: {end - start:.2f} seconds")


def test_exact_recovery(nbits):
    print(f"[-] Testing exact recovery with {nbits} bits")
    random.seed(12345)
    outputs = [random.getrandbits(nbits) for _ in range(N * 32 // nbits)]

    state = [BitVec(f"state_{i}", 32) for i in range(N)]
    sol = Solver()
    for s, o in zip(mt_gen_sol(sol, state), outputs):
        sol.add(LShR(s, 32 - nbits) == o)
    with timeit("z3 solving"):
        assert sol.check() == sat

    m = sol.model()
    state = [m.evaluate(s).as_long() for s in state]

    random.setstate((3, tuple(state + [624]), None))
    for v in outputs:
        assert random.getrandbits(nbits) == v


def test_inexact_recovery(nitems):
    print(f"[-] Testing inexact recovery with {nitems} items")
    random.seed(12345)
    outputs = [(random.randrange(3) + 1) % 3 for _ in range(nitems)]

    state = [BitVec(f"state_{i}", 32) for i in range(N)]
    sol = Solver()
    for s, o in zip(mt_gen_sol(sol, state), outputs):
        sol.add(LShR(s, 30) == o)
    with timeit("z3 solving"):
        assert sol.check() == sat

    m = sol.model()
    state = [m.evaluate(s).as_long() for s in state]

    random.setstate((3, tuple(state + [624]), None))
    for v in outputs:
        assert random.randrange(3) == v


def test_exact_seed_recovery():
    print(f"[-] Testing exact seed recovery")
    random.seed(0x87638763DEADBEEF)
    outputs = [random.getrandbits(32) for _ in range(N)]

    nseeds = 2
    seeds = [BitVec(f"seed_{i}", 32) for i in range(nseeds)]
    state = init_by_array(seeds, len(seeds))
    sol = Solver()
    for s, o in zip(mt_gen_sol(sol, state), outputs):
        sol.add(s == o)
    with timeit("z3 solving"):
        assert sol.check() == sat

    m = sol.model()
    seeds = [m.evaluate(s).as_long() for s in seeds]

    seed = 0
    for s in seeds[::-1]:
        seed <<= 32
        seed += s
    print(f"[-] Recovered seed: {seed:x}")

    random.seed(seed)
    for v in outputs:
        assert random.getrandbits(32) == v


def test_inexact_seed_recovery_slow(nitems):
    # ref: https://blog.maple3142.net/2022/11/13/seccon-ctf-2022-writeups/#janken-vs-kurenaif
    print(f"[-] Testing inexact seed recovery (slow) with {nitems} items")
    random.seed(12345)
    outputs = [(random.randrange(3) + 1) % 3 for _ in range(nitems)]

    nseeds = N
    seeds = [BitVec(f"seed_{i}", 32) for i in range(nseeds)]
    state = random_seed(seeds)
    sol = Solver()
    for s, o in zip(mt_gen_sol(sol, state), outputs):
        sol.add(LShR(s, 30) == o)
    with timeit("z3 solving"):
        assert sol.check() == sat

    m = sol.model()
    seeds = [m.evaluate(s).as_long() for s in seeds]

    seed = 0
    for s in seeds[::-1]:
        seed <<= 32
        seed += s
    print(f"[-] Recovered seed: {seed}")

    random.seed(seed)
    for v in outputs:
        assert random.randrange(3) == v


def test_inexact_seed_recovery_fast(nitems):
    # ref: https://blog.y011d4.com/20221113-seccon-ctf-writeup#janken-vs-kurenaif
    print(f"[-] Testing inexact seed recovery (fast) with {nitems} items")
    random.seed(12345)
    outputs = [(random.randrange(3) + 1) % 3 for _ in range(nitems)]

    state = [BitVec(f"seed_{i}", 32) for i in range(N)]
    sol = Solver()
    sol.add(state[0] == 0x80000000)  # this is really important!!!
    for s, o in zip(mt_gen_sol(sol, state), outputs):
        sol.add(LShR(s, 30) == o)
    with timeit("z3 solving first phase"):
        assert sol.check() == sat

    m = sol.model()
    state = [m.evaluate(s).as_long() for s in state]

    sol = Solver()
    nseeds = N
    seeds = [BitVec(f"seed_{i}", 32) for i in range(nseeds)]
    MT = random_seed(seeds)
    for s, o in zip(MT, state):
        sol.add(s == o)
    with timeit("z3 solving second phase"):
        assert sol.check() == sat

    m = sol.model()
    seeds = [m.evaluate(s).as_long() for s in seeds]

    seed = 0
    for s in seeds[::-1]:
        seed <<= 32
        seed += s
    print(f"[-] Recovered seed: {seed:x}")

    random.seed(seed)
    for v in outputs:
        assert random.randrange(3) == v


if __name__ == "__main__":
    test_exact_recovery(32)
    test_exact_recovery(16)
    test_inexact_recovery(1337)
    test_exact_seed_recovery()
    test_inexact_seed_recovery_fast(666)

    # too slow, but it should works
    # test_inexact_seed_recovery_slow(666)  # about 10 minutes
    # test_exact_recovery(8)  # idk, maybe forever?
