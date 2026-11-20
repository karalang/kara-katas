# LeetCode #1256 bench, in Python: the ★ arm (`num + 1` in binary with its
# leading 1 taken off, the digits found by halving) on 200000 random
# numbers from 0 to 10^9 drawn once, each encoded 20 times; every string's
# length and middle digit folded into a checksum.


def encode(num):
    digits = []
    x = num + 1
    while x > 1:
        digits.append('1' if x % 2 == 1 else '0')
        x //= 2
    return ''.join(reversed(digits))


seed = 1256


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    nums = []
    for _ in range(200000):
        hi = next_random() * 32768
        nums.append((hi + next_random()) % 1000000001)
    check = 0
    for _ in range(20):
        for num in nums:
            s = encode(num)
            mid = 0 if not s else (2 if s[len(s) // 2] == '1' else 1)
            check = (check * 131 + len(s) * 3 + mid) % 1000000007
    print(f"20 rounds of 200000 numbers: checksum {check}")


main()
