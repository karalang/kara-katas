# LeetCode #1529: Minimum Suffix Flips -- mirrors flips.kara (the ★ arm):
# the number of places where a bit differs from its left neighbour, the
# first compared with a 0. O(n).


def min_flips(target):
    flips = 0
    prev = "0"
    for c in target:
        if c != prev:
            flips += 1
            prev = c
    return flips


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most):
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        ones = next_random() % 9 + 1
        target = "".join("1" if next_random() % 10 < ones else "0" for _ in range(n))
        check = mix(check, min_flips(target))
    print(f"{count} strings of 1 to {most} bits: checksum {check}")


def main():
    global seed
    for target in ["10111", "101", "00000", "1", "0110"]:
        print(f"{target} -> {min_flips(target)}")
    alternating = "".join("0" if i % 2 == 0 else "1" for i in range(100000))
    print(f"100000 alternating 0 and 1 -> {min_flips(alternating)}")
    seed = 1529
    batch(3000, 12)
    batch(300, 1000)
    batch(30, 100000)


main()
