# LeetCode #2730: Find the Longest Semi-Repetitive Substring -- the bench
# (semi.kara in Python): a sliding window holding at most one adjacent
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


count, rounds = 200000, 20
strings = []
for _ in range(count):
    digits = next_random() % 9 + 2
    strings.append("".join(chr(ord("0") + next_random() % digits) for _ in range(50)))
total = 0
check = 0
for r in range(rounds):
    for s in strings:
        length = longest_semi_repetitive_substring(s)
        total += length
        check = (check * 31 + length + r) % 1000000007
print(f"{count} strings of 50 digits, {rounds} rounds: lengths sum to {total}, checksum {check}")
