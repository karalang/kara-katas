"""Benchmark workload for LeetCode #261 — Graph Valid Tree (Python mirror).

Mirrors valid_tree.kara algorithm-for-algorithm. Correctness oracle only —
Python is not a measured lane (see BENCHMARKS.md).
"""


def find(parent, x):
    r = x
    while parent[r] != r:
        r = parent[r]
    c = x
    while parent[c] != r:
        parent[c], c = r, parent[c]
    return r


def main():
    n = 100000
    rounds = 240
    m = n - 1

    eu = [0] * m
    ev = [0] * m
    state = 261261
    for i in range(1, n):
        state = (state * 1103515245 + 12345) & 2147483647
        wd1 = state // 65536
        state = (state * 1103515245 + 12345) & 2147483647
        eu[i - 1] = (wd1 * 32768 + state // 65536) % i
        ev[i - 1] = i
    for sh in range(m - 1, 0, -1):
        state = (state * 1103515245 + 12345) & 2147483647
        wd0 = state // 65536
        state = (state * 1103515245 + 12345) & 2147483647
        j = (wd0 * 32768 + state // 65536) % (sh + 1)
        eu[sh], eu[j] = eu[j], eu[sh]
        ev[sh], ev[j] = ev[j], ev[sh]

    sink = 0
    for r in range(rounds):
        parent = list(range(n))
        size = [1] * n

        start = (r * 7919) % m
        components = n
        cyclic = False
        e = 0
        while e < m:
            idx = (start + e) % m
            ra = find(parent, eu[idx])
            rb = find(parent, ev[idx])
            if ra == rb:
                cyclic = True
                e = m
            else:
                if size[ra] < size[rb]:
                    parent[ra] = rb
                    size[rb] += size[ra]
                else:
                    parent[rb] = ra
                    size[ra] += size[rb]
                components -= 1
                e += 1

        acc = 0
        for p in range(n):
            acc = (acc * 31 + parent[p]) % 1000000007
        verdict = 1 if components == 1 and not cyclic else 0
        sink = (sink * 131 + acc + verdict) % 1000000007

    print(sink)


main()
