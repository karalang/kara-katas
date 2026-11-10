# LeetCode #2105: Watering Plants II -- Python mirror of the ★ arm
# (watering.kara): two indices walking in from the ends, each can
# refilled when short, and a middle plant to the fuller can. Prints the
# same lines.


def minimum_refill(plants, capacity_a, capacity_b):
    i, j = 0, len(plants) - 1
    a, b = capacity_a, capacity_b
    refills = 0
    while i < j:
        if a < plants[i]:
            refills += 1
            a = capacity_a
        a -= plants[i]
        if b < plants[j]:
            refills += 1
            b = capacity_b
        b -= plants[j]
        i += 1
        j -= 1
    if i == j and max(a, b) < plants[i]:
        refills += 1
    return refills


seed = 2105


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        ([2, 2, 3, 3], 5, 5),
        ([2, 2, 3, 3], 3, 4),
        ([5], 10, 8),
        ([1, 2, 4, 4, 5], 6, 5),
        ([3, 1, 2, 1, 1], 4, 4),
        ([3, 3, 3, 3, 3, 3], 3, 3),
        ([4, 6], 4, 6),
        ([1, 1, 1, 1, 1], 9, 9),
    ]
    for plants, a, b in examples:
        print(f"{show(plants)} with {a} and {b} -> {minimum_refill(plants, a, b)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 50 + 1
        plants = [next_random() % 10 + 1 for _ in range(n)]
        most = max(plants)
        a = most + next_random() % 6
        b = most + next_random() % 6
        got = minimum_refill(plants, a, b)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"3000 rows: {total} refills, checksum {check}")
    full = [1000000] * 100000
    rising = [i % 1000000 + 1 for i in range(100000)]
    print(f"full -> {minimum_refill(full, 1000000, 1000000)}")
    print(f"rising -> {minimum_refill(rising, 1000000000, 1000000000)}")


main()
