# LeetCode #2269: Find the K-Beauty of a Number -- the Python mirror of
# the ★ arm, `beauty.kara`, line for line. Its output is byte-identical.


def divisor_substrings(num, k):
    s = str(num)
    beauty = 0
    for i in range(len(s) - k + 1):
        part = int(s[i:i + k])
        if part != 0 and num % part == 0:
            beauty += 1
    return beauty


seed = 2269


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for num, k in [(240, 2), (430043, 2), (7, 1), (123456, 6), (1000, 2), (111111111, 3), (1000000000, 1)]:
        print(f"{num}, {k} -> {divisor_substrings(num, k)}")
    total = 0
    check = 0
    for t in range(3000):
        digits = t % 9 + 1
        num = 0
        for _ in range(digits):
            num = num * 10 + next_random() % 10
        if num == 0:
            num = 1
        k = next_random() % len(str(num)) + 1
        b = divisor_substrings(num, k)
        total += b
        check = (check * 31 + b) % 1000000007
    print(f"3000 numbers: total {total}, checksum {check}")
    for num in [1000000000, 999999999, 735134400]:
        alls = [divisor_substrings(num, k) for k in range(1, len(str(num)) + 1)]
        print(f"{num}: [{', '.join(map(str, alls))}]")


main()
