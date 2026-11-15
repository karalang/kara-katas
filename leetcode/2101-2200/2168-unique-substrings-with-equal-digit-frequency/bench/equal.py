# LeetCode #2168: Unique Substrings With Equal Digit Frequency -- the
# benchmark's Python mirror of equal.kara.


def equal_digit_frequency(s):
    n = len(s)
    found = set()
    for i in range(n):
        counts = [0] * 10
        kinds = 0
        most = 0
        for j in range(i, n):
            d = ord(s[j]) - 48
            if counts[d] == 0:
                kinds += 1
            counts[d] += 1
            most = max(most, counts[d])
            if most * kinds == j - i + 1:
                found.add(s[i:j + 1])
    return len(found)


seed = 2168


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    digits = [48 + next_random() % 3 for _ in range(1000)]
    check = 0
    for _ in range(200):
        at = next_random() % 1000
        digits[at] = 48 + next_random() % 3
        check = (check * 31 + equal_digit_frequency(bytes(digits).decode())) % 1000000007
    print(f"200 solves: checksum {check}")


main()
