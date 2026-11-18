# LeetCode #2300: Successful Pairs of Spells and Potions -- the bench,
# the ★ arm in Python. Sort a copy of the potions, then for each spell
# binary-search the first potion whose product with it reaches `success`.

seed = 2300


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def successful_pairs(spells, potions, success):
    s = sorted(potions)
    m = len(s)
    out = []
    for spell in spells:
        lo, hi = 0, m
        while lo < hi:
            mid = (lo + hi) // 2
            if spell * s[mid] < success:
                lo = mid + 1
            else:
                hi = mid
        out.append(m - lo)
    return out


def main():
    spells = []
    potions = []
    for _ in range(10):
        s = []
        p = []
        for _ in range(100000):
            s.append((next_random() * 32768 + next_random()) % 100000 + 1)
            p.append((next_random() * 32768 + next_random()) % 100000 + 1)
        spells.append(s)
        potions.append(p)
    check = 0
    for pas in range(5):
        for c in range(10):
            for x in successful_pairs(spells[c], potions[c], 1000000000 * c + 7 + pas):
                check = (check * 31 + x) % 1000000007
    print(f"5 passes over 10 cases of 10^5 spells and potions: checksum {check}")


main()
