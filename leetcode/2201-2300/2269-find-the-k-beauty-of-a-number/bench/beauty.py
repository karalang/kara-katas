# LeetCode #2269: Find the K-Beauty of a Number -- the bench, the ★ arm.


def divisor_substrings(num, k):
    s = str(num)
    beauty = 0
    for i in range(len(s) - k + 1):
        part = int(s[i:i + k])
        if part != 0 and num % part == 0:
            beauty += 1
    return beauty


# ---- bench harness ---------------------------------------------------------

seed = 2269


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for t in range(200000):
        num = (next_random() * 32768 + next_random()) % 1000000000 + 1
        k = min(t % 9 + 1, len(str(num)))
        check = (check * 31 + divisor_substrings(num, k)) % 1000000007
    print(f"200000 numbers: checksum {check}")


main()
