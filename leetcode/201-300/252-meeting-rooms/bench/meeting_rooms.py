"""Benchmark workload for LeetCode #252 — Meeting Rooms (Python; scale lane)."""


def main():
    n = 120000
    rounds = 40

    base = []
    state = 252252
    cursor = 0
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        dur = (state // 65536) % 7 + 1
        state = (state * 1103515245 + 12345) & 2147483647
        gap = (state // 65536) % 3
        base.append((cursor, cursor + dur))
        cursor += dur + gap
    for k in range(n - 1, 0, -1):
        state = (state * 1103515245 + 12345) & 2147483647
        swap = (state // 65536) % (k + 1)
        base[k], base[swap] = base[swap], base[k]

    sink = 0
    for _ in range(rounds):
        s = list(base)
        s.sort(key=lambda x: x[0])
        ok = True
        for j in range(1, n):
            if s[j][0] < s[j - 1][1]:
                ok = False
        sink = (sink * 31 + 1) % 1000000007 if ok else (sink * 31) % 1000000007
        sink = (sink * 131 + s[n - 1][1] - s[0][0]) % 1000000007
    print(sink)


main()
