# Benchmark: LeetCode #970 Powerful Integers -- the ★ arm, every pair of
# powers in a set, for every x and y from 1 to 100 with bound 10^6.
# Mirrors powerful_integers.kara, .c, .rs and go-seq/.


def powers(base, bound):
    out = []
    p = 1
    while p <= bound:
        out.append(p)
        if base == 1:
            break
        p *= base
    return out


def powerful_integers(x, y, bound):
    seen = set()
    for a in powers(x, bound):
        for b in powers(y, bound - a):
            seen.add(a + b)
    return list(seen)


def main():
    rounds = 100
    found = check = 0
    for r in range(rounds):
        for x in range(1, 101):
            for y in range(1, 101):
                for v in powerful_integers(x, y, 1000000 - r):
                    found += 1
                    check = (check + v * v) % 1000000007
    print(f"{rounds} rounds over x and y from 1 to 100: {found} powerful integers, checksum {check}")


main()
