# LeetCode #1256: Encode Number -- the Python mirror of encode_number.kara:
# `num + 1` in binary with its leading 1 taken off, the digits found by
# halving.


def encode(num):
    digits = []
    x = num + 1
    while x > 1:
        digits.append('1' if x % 2 == 1 else '0')
        x //= 2
    return ''.join(reversed(digits))


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    first = ' '.join(f"[{encode(n)}]" for n in range(8))
    print(f"{encode(23)} {encode(107)} {first}")
    seed = 1256
    length = check = 0
    nums = []
    for _ in range(1000):
        hi = next_random() * 32768
        nums.append((hi + next_random()) % 1000000001)
    nums.extend(range(100000))
    for num in nums:
        s = encode(num)
        length += len(s)
        for c in s:
            check = (check * 3 + (2 if c == '1' else 1)) % 1000000007
    print(f"101000 numbers: {length} digits, checksum {check}")
    print(f"{encode(1000000000)} {encode(1073741822)} {encode(1073741823)}")


main()
