"""Benchmark workload for LeetCode #186 — Reverse Words in a String II (Python; scale lane)."""


def reverse_range(a, lo, hi):
    i = lo
    j = hi
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def reverse_words(a, n):
    if n > 0:
        reverse_range(a, 0, n - 1)
    start = 0
    for i in range(n + 1):
        if i == n or a[i] == 32:
            if i > start:
                reverse_range(a, start, i - 1)
            start = i + 1


def main():
    target_len = 30000
    passes = 3000

    buf = []
    state = 12345
    first = True
    while len(buf) < target_len:
        if first:
            first = False
        else:
            buf.append(32)
        state = (state * 1103515245 + 12345) & 2147483647
        wlen = 1 + (state % 8)
        for _ in range(wlen):
            state = (state * 1103515245 + 12345) & 2147483647
            buf.append(97 + (state % 26))

    n = len(buf)
    modv = 1000000007
    sink = 0
    for p in range(passes):
        idx = (p * 131 + 7) % n
        if buf[idx] != 32:
            buf[idx] = 97 + (((buf[idx] - 97) + 1) % 26)
        reverse_words(buf, n)
        cs = 0
        for k in range(n):
            cs = (cs * 131 + buf[k]) % modv
        sink += cs
    print(sink)


main()
