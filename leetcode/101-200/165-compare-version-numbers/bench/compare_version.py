"""Benchmark workload for LeetCode #165 — Compare Version Numbers (Python; scale lane)."""


def revisions(v):
    revs = []
    n = len(v)
    i = 0
    while i < n:
        val = 0
        while i < n and v[i] != ".":
            val = val * 10 + (ord(v[i]) - ord("0"))
            i += 1
        revs.append(val)
        i += 1  # skip the '.'
    return revs


def compare_version(v1, v2):
    a = revisions(v1)
    b = revisions(v2)
    na = len(a)
    nb = len(b)
    m = na if na > nb else nb
    for i in range(m):
        x = a[i] if i < na else 0
        y = b[i] if i < nb else 0
        if x < y:
            return -1
        if x > y:
            return 1
    return 0


def main():
    m = 4096
    passes = 10000000
    pool = []
    state = 12345
    for _k in range(m):
        state = (state * 1103515245 + 12345) & 2147483647
        r = 1 + (state % 4)
        parts = []
        for t in range(r):
            state = (state * 1103515245 + 12345) & 2147483647
            rev = state % 1000
            parts.append(str(rev))
        pool.append(".".join(parts))
    sink = 0
    for _p in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        i = state % m
        state = (state * 1103515245 + 12345) & 2147483647
        j = state % m
        sink += compare_version(pool[i], pool[j]) + 1
    print(sink)


main()
