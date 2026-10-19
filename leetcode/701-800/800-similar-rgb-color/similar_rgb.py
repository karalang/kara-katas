# LeetCode 800 -- Similar RGB Color: mirrors the harness of
# similar_rgb.kara with the ★ arm, each part rounded.
seed = 800


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def similar_rgb(color):
    digits = "0123456789abcdef"
    out = "#"
    for p in range(3):
        part = int(color[1 + 2 * p:3 + 2 * p], 16)
        k = (part + 8) // 17
        out += digits[k] * 2
    return out


def show(color):
    print(f"{color} -> {similar_rgb(color)}")


def main():
    for c in ["#09f166", "#4e3fe1", "#000000", "#ffffff", "#080808", "#090909", "#f7f7f7", "#123456", "#abcdef"]:
        show(c)
    digits = "0123456789abcdef"
    same = 0
    check = 0
    for i in range(300):
        color = "#"
        for _ in range(3):
            d = digits[next_random() % 16]
            color += d
            color += digits[next_random() % 16] if i % 2 == 0 else d
        got = similar_rgb(color)
        if got == color:
            same += 1
        for c in got.encode():
            check = (check * 131 + c) % 1000000007
    print(f"300 random colours: {same} already shorthand, checksum {check}")


main()
