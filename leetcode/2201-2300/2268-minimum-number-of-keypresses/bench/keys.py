# LeetCode #2268: Minimum Number of Keypresses -- the bench, the ★ arm.


def minimum_keypresses(s):
    count = [0] * 26
    for b in s.encode():
        count[b - 97] += 1
    count.sort(reverse=True)
    total = 0
    for i, c in enumerate(count):
        total += c * (i // 9 + 1)
    return total


# ---- bench harness ---------------------------------------------------------

seed = 2268


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for t in range(40):
        k = [3, 10, 12, 26][t % 4]
        s = "".join(chr(97 + next_random() % k) for _ in range(100000))
        check = (check * 31 + minimum_keypresses(s)) % 1000000007
    print(f"40 strings of 10^5: checksum {check}")


main()
