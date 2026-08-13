"""Benchmark workload for LeetCode #256 — Paint House (Python; scale lane)."""


def main():
    n = 4000000
    rounds = 30

    cost = []
    state = 256256
    cheap = 0
    run_left = 0
    for _ in range(n):
        if run_left == 0:
            state = (state * 1103515245 + 12345) & 2147483647
            run_left = (state // 65536) % 9 + 2
            state = (state * 1103515245 + 12345) & 2147483647
            cheap = (state // 65536) % 3
        state = (state * 1103515245 + 12345) & 2147483647
        lo = (state // 65536) % 10 + 1
        state = (state * 1103515245 + 12345) & 2147483647
        m1 = (state // 65536) % 40 + 40
        state = (state * 1103515245 + 12345) & 2147483647
        m2 = (state // 65536) % 40 + 40
        if cheap == 0:
            cost.append((lo, m1, m2))
        elif cheap == 1:
            cost.append((m1, lo, m2))
        else:
            cost.append((m1, m2, lo))
        run_left -= 1

    sink = 0
    for _ in range(rounds):
        a, b, c = cost[0]
        for k in range(1, n):
            na = cost[k][0] + min(b, c)
            nb = cost[k][1] + min(a, c)
            nc = cost[k][2] + min(a, b)
            a, b, c = na, nb, nc
        sink = (sink * 31 + min(a, b, c)) % 1000000007
    print(sink)


main()
