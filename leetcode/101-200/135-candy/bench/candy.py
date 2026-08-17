"""Benchmark harness for LeetCode #135 — Candy.

Mirrors candy.kara algorithm-for-algorithm, including the explicit descending
index loop for the right-to-left pass. Committed as the correctness oracle; not
a measured lane.
"""

NP = 8
N = 200000
ITERS = 150


def candy(ratings):
    n = len(ratings)
    if n == 0:
        return 0
    c = [1] * n

    i = 1
    while i < n:
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1
        i += 1

    i = n - 2
    while i >= 0:
        if ratings[i] > ratings[i + 1] and c[i] <= c[i + 1]:
            c[i] = c[i + 1] + 1
        i -= 1

    total = 0
    for i in range(n):
        total += c[i]
    return total


def lcg(seed, n, cap):
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        wd0 = x // 65536
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((wd0 * 32768 + x // 65536) % cap)
    return out


def main():
    arrays = []
    for j in range(NP):
        arrays.append(lcg(j + 1, N, 4 if j % 2 == 0 else 100000))

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % NP
        sink = (sink + candy(arrays[idx])) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
