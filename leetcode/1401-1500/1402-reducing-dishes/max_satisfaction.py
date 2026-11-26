# LeetCode #1402: Reducing Dishes -- Python mirror of the ★ arm and its
# harness.


def max_satisfaction(satisfaction):
    order = sorted(satisfaction, reverse=True)
    running = 0
    total = 0
    for s in order:
        if running + s <= 0:
            break
        running += s
        total += running
    return total


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, lo, hi):
    return [lo + next_random() % (hi - lo + 1) for _ in range(n)]


def main():
    global seed
    shown = [
        max_satisfaction([-1, -8, 0, 5, -9]),
        max_satisfaction([4, 3, 2]),
        max_satisfaction([-1, -4, -5]),
        max_satisfaction([0]),
        max_satisfaction([-2, 5, -1, 0, 3, -3]),
        max_satisfaction([1000, -1000]),
    ]
    print(" ".join(str(k) for k in shown))
    seed = 1402
    top = [1000] * 500
    bottom = [-1000] * 500
    big = drawn(500, -1000, 1000)
    print(f"500 dishes: {max_satisfaction(top)} {max_satisfaction(bottom)} {max_satisfaction(big)}")
    check = 0
    total = 0
    for i in range(2000):
        n = 1 + next_random() % 30
        hi = 1000 if i % 2 == 0 else 100
        best = max_satisfaction(drawn(n, -1000, hi))
        total += best
        check = (check * 131 + best) % 1000000007
    print(f"2000 random cases: {total} in all, checksum {check}")


main()
