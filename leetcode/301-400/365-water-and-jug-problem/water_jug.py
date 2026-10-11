# LeetCode #365: Water and Jug Problem -- mirror of water_jug.kara.


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def can_measure_water(x, y, target):
    return target <= x + y and target % gcd(x, y) == 0


def show(label, x, y, target):
    print(f"{label}: {'true' if can_measure_water(x, y, target) else 'false'}")


def main():
    show("example 1", 3, 5, 4)
    show("example 2", 2, 6, 5)
    show("example 3", 1, 2, 3)
    show("both jugs full", 4, 9, 13)
    show("more than both jugs hold", 4, 9, 14)
    show("one jug's capacity", 6, 10, 6)
    show("equal jugs, their capacity", 7, 7, 7)
    show("equal jugs, something else", 7, 7, 3)
    show("coprime jugs reach every amount", 8, 13, 1)
    show("not a multiple of the gcd", 6, 15, 10)
    show("a multiple of the gcd", 6, 15, 12)
    show("a one-litre jug", 1, 1000, 999)
    seed = 365
    yes = 0
    checksum = 0
    for _ in range(3000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        x = 1 + (seed // 65536) % 60
        seed = (seed * 1103515245 + 12345) % 2147483648
        y = 1 + (seed // 65536) % 60
        seed = (seed * 1103515245 + 12345) % 2147483648
        target = 1 + (seed // 65536) % 130
        ok = can_measure_water(x, y, target)
        yes += ok
        checksum = (checksum * 2 + (1 if ok else 0)) % 1000000007
    print(f"3000 random triples: {yes} measurable, checksum {checksum}")


main()
