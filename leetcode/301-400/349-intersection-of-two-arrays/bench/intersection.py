# Benchmark workload for LeetCode #349 — Python mirror of intersection.kara.

POOL = 1000000
LEN = 1000
PAIRS = 20000


def intersection(a, b):
    seen = set()
    for x in a:
        seen.add(x)
    out = []
    for y in b:
        if y in seen:
            seen.remove(y)
            out.append(y)
    out.sort()
    return out


def main():
    pool = []
    x = 349
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
        r = intersection(a, b)
        sink = (sink * 31 + len(r) * 1000003 + sum(r)) % 1000000007
    print(f"sink {sink}")


main()
