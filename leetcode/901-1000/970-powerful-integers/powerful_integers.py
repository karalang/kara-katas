# LeetCode #970: Powerful Integers -- Python mirror of powerful_integers.kara.


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


# ---- test harness -----------------------------------------------------------


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    examples = [
        (2, 3, 10),
        (3, 5, 15),
        (1, 1, 1),
        (1, 1, 2),
        (2, 3, 0),
        (1, 2, 10),
        (3, 1, 30),
        (2, 2, 20),
        (100, 100, 1000000),
        (10, 7, 120),
    ]
    for x, y, bound in examples:
        got = sorted(powerful_integers(x, y, bound))
        print(f"x = {x}, y = {y}, bound = {bound}: {show(got)}")
    for bound in [100, 1000000]:
        count = total = check = 0
        for x in range(1, 101):
            for y in range(1, 101):
                got = sorted(powerful_integers(x, y, bound))
                count += len(got)
                for v in got:
                    total += v
                    check = (check * 31 + v) % 1000000007
        print(f"x and y from 1 to 100, bound {bound}: {count} powerful integers summing to {total}, checksum {check}")
    for x, y in [(2, 3), (2, 2), (2, 1), (1, 1), (3, 99)]:
        got = sorted(powerful_integers(x, y, 1000000))
        check = 0
        for v in got:
            check = (check * 31 + v) % 1000000007
        largest = got[-1] if got else 0
        print(f"x = {x}, y = {y}, bound = 1000000: {len(got)} powerful integers, largest {largest}, checksum {check}")


main()
