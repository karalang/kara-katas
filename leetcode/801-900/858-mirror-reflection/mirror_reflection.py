# LeetCode #858: Mirror Reflection -- Python mirror of the ★ arm (halve both
# lengths while both are even, then read the receptor off their parities).


def mirror_reflection(p, q):
    while p % 2 == 0 and q % 2 == 0:
        p //= 2
        q //= 2
    if p % 2 == 0:
        return 2
    if q % 2 == 0:
        return 0
    return 1


def show(p, q):
    print(f"p = {p}, q = {q} -> {mirror_reflection(p, q)}")


seed = 858


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for p, q in [(2, 1), (3, 1), (1, 1), (4, 2), (6, 4), (5, 5), (1000, 1), (999, 1), (1000, 999),
                 (1000, 250), (750, 500), (999, 333), (1000, 1000)]:
        show(p, q)
    counts = [0, 0, 0]
    for p in range(1, 101):
        for q in range(1, p + 1):
            counts[mirror_reflection(p, q)] += 1
    print(f"all 5050 rooms of side up to 100: receptor 0 {counts[0]} times, 1 {counts[1]}, 2 {counts[2]}")
    total = 0
    check = 0
    for _ in range(300):
        p = 1 + next_random() % 1000
        q = 1 + next_random() % p
        r = mirror_reflection(p, q)
        total += r
        check = (check * 31 + r * 1000 + q) % 1000000007
    print(f"300 random rooms of side up to 1000: receptors sum to {total}, checksum {check}")


main()
