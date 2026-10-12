# Benchmark for #396: mirror of rotate_function.kara (one rotation from the last).
# Python's % takes the sign of the divisor, Kara's and C's of the dividend, so
# the pool values and the checksum use helpers that truncate like C.
import sys


def cmod(a, b):
    r = abs(a) % b
    return -r if a < 0 else r


def max_rotate_function(nums, lo, hi):
    n = hi - lo
    s = 0
    f = 0
    for i in range(n):
        v = nums[lo + i]
        s += v
        f += i * v
    best = f
    for k in range(1, n):
        f = f + s - n * nums[lo + n - k]
        if f > best:
            best = f
    return best


seed = 396


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    windows = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    pool = [step() % 201 - 100 for _ in range(1000000)]
    m = 1000000007
    total = 0
    checksum = 0
    for _ in range(windows):
        hi = step()
        a = (hi * 32768 + step()) % (1000000 - 100000)
        r = max_rotate_function(pool, a, a + 100000)
        total += r
        checksum = (checksum * 31 + cmod(r, m) + m) % m
    print(f"{windows} windows: total {total}, checksum {checksum}")


main()
