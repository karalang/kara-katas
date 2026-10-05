# Benchmark workload for LeetCode #350 — Python mirror of intersect.kara.

POOL = 1000000
LEN = 1000
PAIRS = 20000


def intersect(a, b):
    counts = {}
    for x in a:
        counts[x] = counts.get(x, 0) + 1
    out = []
    for y in b:
        left = counts.get(y, 0)
        if left > 0:
            counts[y] = left - 1
            out.append(y)
    out.sort()
    return out


def main():
    pool = []
    x = 350
    for _ in range(POOL):
        x = (x * 1103515245 + 12345) % 2147483648
        pool.append(x // 16 % 1001)

    sink = 0
    for _ in range(PAIRS):
        x = (x * 1103515245 + 12345) % 2147483648
        i = x // 16 % (POOL - LEN)
        x = (x * 1103515245 + 12345) % 2147483648
        j = x // 16 % (POOL - LEN)
        a = pool[i:i + LEN]
        b = pool[j:j + LEN]
        r = intersect(a, b)
        sink = (sink * 31 + len(r) * 1000003 + sum(r)) % 1000000007
    print(f"sink {sink}")


main()
