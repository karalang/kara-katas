# LeetCode #1737: Change Minimum Characters to Satisfy One of Three
# Conditions -- mirrors minimum.kara (the ★ arm).


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


def word(most, letters):
    n = (next_random() * 32768 + next_random()) % most + 1
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def batch(count, most, letters):
    total = 0
    check = 0
    for _ in range(count):
        a = word(most, letters)
        b = word(most, letters)
        answer = min_characters(a, b)
        total += answer
        check = (check * 31 + answer + len(a)) % 1000000007
    print(f"{count} pairs of up to {most} letters from {letters}: changes sum to {total}, checksum {check}")


print(min_characters("aba", "caa"))
print(min_characters("dabadd", "cda"))
print(min_characters("a", "b"))
print(min_characters("aaa", "aa"))
print(min_characters("zz", "a"))
print(min_characters("az", "az"))
batch(3000, 6, 4)
batch(1000, 100, 26)
batch(10, 100000, 26)
