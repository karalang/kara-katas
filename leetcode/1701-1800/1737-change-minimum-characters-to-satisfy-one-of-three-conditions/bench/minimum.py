# LeetCode #1737: Change Minimum Characters to Satisfy One of Three
# Conditions -- the bench (minimum.kara): letter counts, and every
# boundary tried.


def min_characters(a, b):
    count_a = [0] * 26
    count_b = [0] * 26
    for c in a:
        count_a[ord(c) - 97] += 1
    for c in b:
        count_b[ord(c) - 97] += 1
    m, n = len(a), len(b)
    best = m + n
    for c in range(26):
        best = min(best, m + n - count_a[c] - count_b[c])
    below_a = 0
    below_b = 0
    for c in range(1, 26):
        below_a += count_a[c - 1]
        below_b += count_b[c - 1]
        best = min(best, m - below_a + below_b)
        best = min(best, n - below_b + below_a)
    return best


seed = 1737


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count = 20
rounds = 200
n = 100000
problems = []
for _ in range(count):
    a = "".join(chr(97 + next_random() % 26) for _ in range(n))
    b = "".join(chr(97 + next_random() % 26) for _ in range(n))
    problems.append((a, b))
total = 0
check = 0
for r in range(rounds):
    for a, b in problems:
        answer = min_characters(a, b)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} pairs of {n} letters, {rounds} rounds: changes sum to {total}, checksum {check}")
