# LeetCode #1638: Count Substrings That Differ by One Character -- the
# Python mirror of the ★ arm: matching runs ending and starting at each
# pair of positions, and (left + 1) * (right + 1) for every mismatch.


def count_substrings(s, t):
    n, m = len(s), len(t)
    left = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            if s[i] == t[j]:
                left[i + 1][j + 1] = left[i][j] + 1
    right = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s[i] == t[j]:
                right[i][j] = right[i + 1][j + 1] + 1
    count = 0
    for i in range(n):
        for j in range(m):
            if s[i] != t[j]:
                count += (left[i][j] + 1) * (right[i + 1][j + 1] + 1)
    return count


# ---- the harness: the same as every arm's ---------------------------------

seed = 1638


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(most, letters):
    n = next_random() % most + 1
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def batch(count, most, letters):
    check = 0
    total = 0
    for _ in range(count):
        s = random_word(most, letters)
        t = random_word(most, letters)
        pairs = count_substrings(s, t)
        total += pairs
        check = (check * 31 + pairs + 1) % 1000000007
    print(f"{count} pairs of up to {most} letters: counts sum to {total}, checksum {check}")


print(count_substrings("aba", "baba"))
print(count_substrings("ab", "bb"))
print(count_substrings("a", "a"))
print(count_substrings("abe", "bbc"))
print(count_substrings("aaa", "bbb"))
batch(3000, 6, 2)
batch(300, 100, 3)
batch(20, 100, 26)
