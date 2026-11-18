# LeetCode #2300: Successful Pairs of Spells and Potions -- mirror of the
# ★ arm (pairs.kara): the potions sorted once, and for each spell the
# first potion whose product with it reaches `success` found by binary
# search.


def partition_point(v, pred):
    lo, hi = 0, len(v)
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(v[mid]):
            lo = mid + 1
        else:
            hi = mid
    return lo


def successful_pairs(spells, potions, success):
    s = sorted(potions)
    m = len(s)
    return [m - partition_point(s, lambda p: spell * p < success) for spell in spells]


# ---- test harness ----------------------------------------------------------

seed = 2300


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [
        ([5, 1, 3], [1, 2, 3, 4, 5], 7),
        ([3, 1, 2], [8, 5, 8], 16),
        ([4, 9], [2, 7, 7], 1),
        ([100000, 99999, 1], [100000, 7, 100000], 10000000000),
        ([1, 2, 3], [1, 2], 7),
    ]
    for spells, potions, success in cases:
        print(show(successful_pairs(spells, potions, success)))
    check = 0
    total = 0
    for _ in range(2000):
        spells = [next_random() % 50 + 1 for _ in range(next_random() % 40 + 1)]
        potions = [next_random() % 50 + 1 for _ in range(next_random() % 40 + 1)]
        success = next_random() % 2600 + 1
        for x in successful_pairs(spells, potions, success):
            check = (check * 31 + x) % 1000000007
            total += x
    print(f"2000 cases: checksum {check}, sum {total}")


main()
