# LeetCode #2745: Construct the Longest New String -- Python mirror of
# longest.kara (the ★ arm): the "AA"s and "BB"s alternate, all of the
# fewer and one more of the other, and every "AB" fits.


def longest_string(x, y, z):
    alternating = 2 * x if x == y else 2 * min(x, y) + 1
    return (alternating + z) * 2


seed = 2745


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(longest_string(2, 5, 1))
    print(longest_string(3, 2, 2))
    print(longest_string(1, 1, 1))
    print(longest_string(7, 7, 3))
    print(longest_string(50, 50, 50))
    total = check = 0
    for x in range(1, 13):
        for y in range(1, 13):
            for z in range(1, 13):
                length = longest_string(x, y, z)
                total += length
                check = (check * 31 + length) % 1000000007
    print(f"1728 small counts: lengths sum to {total}, checksum {check}")
    total = check = 0
    for _ in range(100):
        x = next_random() % 50 + 1
        y = next_random() % 50 + 1
        z = next_random() % 50 + 1
        length = longest_string(x, y, z)
        total += length
        check = (check * 31 + length) % 1000000007
    print(f"100 counts up to 50: lengths sum to {total}, checksum {check}")


main()
