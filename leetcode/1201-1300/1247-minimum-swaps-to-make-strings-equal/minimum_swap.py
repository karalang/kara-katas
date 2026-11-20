# LeetCode #1247: Minimum Swaps to Make Strings Equal -- mirrors
# minimum_swap.kara.


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
    a = minimum_swap("xx", "yy")
    b = minimum_swap("xy", "yx")
    c = minimum_swap("xx", "xy")
    d = minimum_swap("xxyyxyxyxx", "xyyxyxxxyx")
    print(f"{a} {b} {c} {d}")
    total = 0
    impossible = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 1000 + 1
        p1 = next_random() % 101
        p2 = next_random() % 101
        s1 = random_xy(n, p1)
        s2 = random_xy(n, p2)
        swaps = minimum_swap(s1, s2)
        if swaps < 0:
            impossible += 1
        else:
            total += swaps
        check = (check * 131 + swaps + 1) % 1000000007
    print(f"1000 random pairs: {impossible} impossible, total {total}, checksum {check}")
    half = "xy" * 500
    flipped = "yx" * 500
    all_x = "x" * 1000
    all_y = "y" * 1000
    print(f"1000 letters: crossed {minimum_swap(half, flipped)}, one way {minimum_swap(all_x, all_y)}")


main()
