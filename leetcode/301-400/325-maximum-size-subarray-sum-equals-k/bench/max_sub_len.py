"""Benchmark workload for LeetCode #325 — Python mirror of max_sub_len.kara.

A fresh dict per call, `get` for the lookup, `setdefault` for the
first-occurrence insert.
"""

LEN = 200000
PUNCHES = 60
MODULUS = 1073741789


def max_sub_len(nums, k):
    first = {0: -1}
    p = 0
    best = 0
    for i, x in enumerate(nums):
        p += x
        j = first.get(p - k)
        if j is not None and i - j > best:
            best = i - j
        first.setdefault(p, i)
    return best


seed = 325


def nxt():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def tdiv(a, b):
    """Integer division truncating toward zero, as Kara's `/` does."""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def main():
    ranges = [1, 100, 10000]
    arrays = [[nxt() % (2 * r + 1) - r for _ in range(LEN)] for r in ranges]
    sink = 0
    for punch in range(PUNCHES):
        t = punch % 3
        r = ranges[t]
        hi = nxt()
        pos = (hi * 32768 + nxt()) % LEN
        arrays[t][pos] = nxt() % (2 * r + 1) - r
        k = tdiv((nxt() % 41 - 20) * r, 4)
        sink = (sink * 31 + max_sub_len(arrays[t], k) + 1) % MODULUS
    print(f"sink {sink}")


main()
