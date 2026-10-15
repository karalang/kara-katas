# LeetCode #680: Valid Palindrome II -- two pointers. Bench.


def is_palindrome(s, i, j):
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


def valid_palindrome(s):
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return is_palindrome(s, i + 1, j) or is_palindrome(s, i, j - 1)
        i += 1
        j -= 1
    return True


def main():
    count, length, rounds = 300, 20000, 100
    widths = [2, 3, 26]
    seed = 680

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    strings = []
    for k in range(count):
        width = widths[k % 3]
        extra = k // 3 % 3
        cs = [chr(97 + next_random() % width) for _ in range(length // 2)]
        cs.extend(reversed(cs))
        for _ in range(extra):
            at = next_random() % (len(cs) + 1)
            cs.insert(at, chr(97 + next_random() % width))
        strings.append("".join(cs))
    valid = 0
    total = 0
    for r in range(rounds):
        for k in range(count):
            at = (k * 7 + r) % count
            if valid_palindrome(strings[at]):
                valid += 1
                total = (total * 31 + at + 1) % 1000000007
            else:
                total = (total * 31 + 7) % 1000000007
    print(f"{count * rounds} strings checked: {valid} valid, checksum {total}")


main()
