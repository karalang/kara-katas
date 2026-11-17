# LeetCode #1187: Make Array Strictly Increasing -- the Python mirror of the
# ★ arm: for each count k of replacements, the least value the prefix can
# end on. Every answer but the last two lines' is also checked against the
# statement read literally: every choice, for each element, of keeping it or
# replacing it with a value of arr2, for arrays of at most 6 values.
from bisect import bisect_right
from itertools import product

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


def literal(arr1, arr2):
    best = -1
    for choice in product(*[[a] + list(arr2) for a in arr1]):
        if all(x < y for x, y in zip(choice, choice[1:])):
            # a replacement by an equal value is no replacement
            k = sum(1 for a, c in zip(arr1, choice) if c != a)
            if best < 0 or k < best:
                best = k
    return best


def checked(arr1, arr2):
    got = make_array_increasing(arr1, arr2)
    if len(arr1) <= 6 and len(arr2) <= 6:
        want = literal(arr1, arr2)
        assert got == want, (arr1, arr2, got, want)
    return got


seed = 0


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


print(f"example 1: {checked([1, 5, 3, 6, 7], [1, 3, 2, 4])}")
print(f"example 2: {checked([1, 5, 3, 6, 7], [4, 3, 1])}")
print(f"example 3: {checked([1, 5, 3, 6, 7], [1, 6, 3, 3])}")
print(f"small 1: {checked([5], [1])}")
print(f"small 2: {checked([3, 2, 1], [1, 2, 3])}")
print(f"small 3: {checked([3, 3, 3], [3])}")
print(f"small 4: {checked([0, 1000000000, 0], [1000000000, 999999999])}")
seed = 1187
checksum = 0
for t in range(2000):
    n = 1 + next_random() % 8
    m = 1 + next_random() % 8
    span = 2 + next_random() % 12
    arr1 = values(n, span)
    arr2 = values(m, span)
    checksum = (checksum * 31 + checked(arr1, arr2) + 2 + t) % 1000000007
print(f"2000 random pairs: checksum {checksum}")
arr1 = values(2000, 1000000001)
arr2 = values(2000, 1000000001)
print(f"2000 and 2000 values: {make_array_increasing(arr1, arr2)}")
rising = [i * 500000 for i in range(2000)]
rising[1000] = 0
print(f"2000 rising, one dip: {make_array_increasing(rising, [1, 499999999, 499999998])}")
