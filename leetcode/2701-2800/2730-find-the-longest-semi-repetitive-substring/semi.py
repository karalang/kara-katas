# LeetCode #2730: Find the Longest Semi-Repetitive Substring -- the ★ arm
# (semi.kara) in Python: a sliding window holding at most one adjacent
# equal pair.


def longest_semi_repetitive_substring(s):
    left = 0
    pairs = 0
    best = 1
    for right in range(1, len(s)):
        if s[right] == s[right - 1]:
            pairs += 1
        while pairs > 1:
            if s[left] == s[left + 1]:
                pairs -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


seed = 2730


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_digits(n, digits):
    return "".join(chr(ord("0") + next_random() % digits) for _ in range(n))


print(longest_semi_repetitive_substring("52233"))
print(longest_semi_repetitive_substring("5494"))
print(longest_semi_repetitive_substring("1111111"))
print(longest_semi_repetitive_substring("7"))
print(longest_semi_repetitive_substring("1" * 50))
print(longest_semi_repetitive_substring("0123456789" * 5))
print(longest_semi_repetitive_substring("00" + "12" * 23 + "00"))
print(longest_semi_repetitive_substring("112" * 16))
total = 0
check = 0
for _ in range(5000):
    n = next_random() % 50 + 1
    digits = next_random() % 10 + 1
    length = longest_semi_repetitive_substring(random_digits(n, digits))
    total += length
    check = (check * 31 + length) % 1000000007
print(f"5000 strings: lengths sum to {total}, checksum {check}")
