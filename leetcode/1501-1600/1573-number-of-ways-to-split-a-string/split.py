# LeetCode #1573: Number of Ways to Split a String -- the Python mirror of
# the ★ arm: with t ones in all, each part holds t / 3, and the answer is
# the product of the gap after the (t/3)-th one and the gap after the
# (2t/3)-th; with no ones, every pair of the n - 1 cut points works. O(n)


def num_ways(s):
    m = 1000000007
    ones = [i for i, c in enumerate(s) if c == "1"]
    n = len(s)
    t = len(ones)
    if t == 0:
        return (n - 1) * (n - 2) // 2 % m
    if t % 3 != 0:
        return 0
    k = t // 3
    return (ones[k] - ones[k - 1]) * (ones[2 * k] - ones[2 * k - 1]) % m


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, sparse):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (most - 2) + 3
        odds = next_random() % sparse + 1
        s = "".join("1" if next_random() % odds == 0 else "0" for _ in range(n))
        ways = num_ways(s)
        total += ways
        check = mix(check, ways)
    print(f"{count} strings of up to {most} characters: ways total {total}, checksum {check}")


def main():
    global seed
    examples = ["10101", "1001", "0000", "100100010100110", "111", "000", "1101010", "1001001"]
    for s in examples:
        print(f"{s} -> {num_ways(s)}")
    seed = 1573
    batch(3000, 12, 3)
    batch(300, 1000, 10)
    batch(30, 100000, 100)
    print(f"100000 zeros -> {num_ways('0' * 100000)}")


main()
