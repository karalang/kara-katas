# LeetCode #1196: How Many Apples Can You Put into the Basket -- the ★ arm
# in Python: the weights sorted, and the lightest put in one at a time until
# the next would take the load past 5000.


def max_number_of_apples(weight):
    weight = sorted(weight)
    load = 0
    for i, w in enumerate(weight):
        load += w
        if load > 5000:
            return i
    return len(weight)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def weights(n, low, high):
    return [low + next_random() % (high - low + 1) for _ in range(n)]


def main():
    global seed
    cases = [
        [100, 200, 150, 1000],
        [900, 950, 800, 1000, 700, 800],
        [1000, 1000, 1000, 1000, 1000],
        [1000, 1000, 1000, 1000, 1000, 1000],
        [1],
        [1000, 1000, 1000, 1000, 999, 1],
        [1000, 1000, 1000, 1000, 999, 2],
        [1000, 1, 1000, 1, 1000, 1, 1000, 1, 1000, 1],
    ]
    for c in cases:
        print(f"[{', '.join(map(str, c))}]: {max_number_of_apples(c)}")
    print(f"1000 apples of 1: {max_number_of_apples([1] * 1000)}")
    print(f"1000 apples of 1000: {max_number_of_apples([1000] * 1000)}")
    seed = 1196
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 40 + 1
        high = [10, 100, 400, 1000][next_random() % 4]
        apples = max_number_of_apples(weights(n, 1, high))
        total += apples
        check = (check * 131 + apples + 1) % 1000000007
    print(f"2000 random baskets: {total} apples, checksum {check}")
    print(f"1000 apples of 1 to 1000: {max_number_of_apples(weights(1000, 1, 1000))}")
    print(f"1000 apples of 1 to 20: {max_number_of_apples(weights(1000, 1, 20))}")


main()
