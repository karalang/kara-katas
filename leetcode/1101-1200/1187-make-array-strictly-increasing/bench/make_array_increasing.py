# LeetCode #1187: Make Array Strictly Increasing -- the bench, in Python: the
# ★ arm's algorithm (for each count k of replacements, the least value the
# prefix can end on) over the same pairs as the Kāra bench.
from bisect import bisect_right

NONE = 2**63 - 1


def make_array_increasing(arr1, arr2):
    spare = sorted(set(arr2))
    n = len(arr1)
    end = [NONE] * (n + 1)
    end[0] = -(2**63)
    for a in arr1:
        nxt = [NONE] * (n + 1)
        for k in range(n + 1):
            if end[k] != NONE and a > end[k]:
                nxt[k] = a
            if k > 0 and end[k - 1] != NONE:
                p = bisect_right(spare, end[k - 1])
                if p < len(spare) and spare[p] < nxt[k]:
                    nxt[k] = spare[p]
        end = nxt
    for k in range(n + 1):
        if end[k] != NONE:
            return k
    return -1


seed = 1187


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def values(n, span):
    out = []
    for _ in range(n):
        hi = next_random()
        out.append((hi * 32768 + next_random()) % span)
    return out


firsts, seconds = [], []
firsts.append(values(2000, 1000000001))
seconds.append(values(2000, 1000000001))
firsts.append([0 if i % 40 == 39 else i * 500000 for i in range(2000)])
seconds.append(values(2000, 1000000001))
firsts.append(values(2000, 4000))
seconds.append(values(2000, 4000))
firsts.append([(2000 - i) * 1000 for i in range(2000)])
seconds.append(values(2000, 1000000001))
rounds = 6
check = 0
for rnd in range(rounds):
    for p in range(4):
        ops = make_array_increasing(firsts[p], seconds[p])
        check = (check * 131 + ops + 2 + rnd) % 1000000007
print(f"{rounds} rounds of 4 pairs of 2000 values: checksum {check}")
