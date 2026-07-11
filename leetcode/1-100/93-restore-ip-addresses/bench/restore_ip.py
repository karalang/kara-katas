"""Benchmark workload — Restore IP Addresses (LeetCode #93).

Python mirror of bench/restore_ip.kara. Folds the segment values of every valid
four-segment quadruple through a rolling polynomial hash; digits computed inline. Input
length varies per iteration (n = 4 + iter%9). Smaller K (pure-Python is slow); timed
separately, NOT cross-checked. See ../README.md.
"""


def digit(pos, iter_):
    return (pos * 7 + iter_) % 10


def seg_val(start, length, iter_):
    if length < 1 or length > 3:
        return -1
    if length > 1 and digit(start, iter_) == 0:
        return -1
    v = 0
    for i in range(length):
        v = v * 10 + digit(start + i, iter_)
    if v > 255:
        return -1
    return v


def restore_fold(n, iter_, seed):
    acc = seed
    a = 1
    while a <= 3 and a < n:
        v0 = seg_val(0, a, iter_)
        if v0 >= 0:
            b = a + 1
            while b <= a + 3 and b < n:
                v1 = seg_val(a, b - a, iter_)
                if v1 >= 0:
                    c = b + 1
                    while c <= b + 3 and c < n:
                        v2 = seg_val(b, c - b, iter_)
                        v3 = seg_val(c, n - c, iter_)
                        if v2 >= 0 and v3 >= 0:
                            acc = (acc * 131 + v0 * 1000000 + v1 * 10000 + v2 * 100 + v3 + 1) % 1000000007
                        c += 1
                b += 1
        a += 1
    return acc


def main():
    total = 200000
    modulus = 1000000007
    total_sum = 0
    for it in range(total):
        n = 4 + (it % 9)  # 4..12 — data-dependent length
        total_sum = (total_sum * 131 + restore_fold(n, it, it)) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
