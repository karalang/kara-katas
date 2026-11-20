# LeetCode #1247 bench, in Python: the ★ arm (the places that differ
# counted by kind over the two strings zipped) on 2000 random pairs of
# 1000 letters built once, each with its own mix of x and y, each asked 20
# times; every answer folded into a checksum.


def minimum_swap(s1, s2):
    x_over_y = 0
    y_over_x = 0
    for a, b in zip(s1, s2):
        if a == "x" and b == "y":
            x_over_y += 1
        elif a == "y" and b == "x":
            y_over_x += 1
    if (x_over_y + y_over_x) % 2 == 1:
        return -1
    return x_over_y // 2 + y_over_x // 2 + 2 * (x_over_y % 2)


seed = 1247


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_xy(n, percent):
    return "".join("x" if next_random() % 100 < percent else "y" for _ in range(n))


def main():
    pairs = []
    for _ in range(2000):
        p1 = next_random() % 101
        p2 = next_random() % 101
        s1 = random_xy(1000, p1)
        s2 = random_xy(1000, p2)
        pairs.append((s1, s2))
    check = 0
    for _ in range(20):
        for s1, s2 in pairs:
            check = (check * 131 + minimum_swap(s1, s2) + 1) % 1000000007
    print(f"20 rounds of 2000 pairs of 1000 letters: checksum {check}")


main()
