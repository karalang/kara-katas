# LeetCode #1638: Count Substrings That Differ by One Character -- the
# bench's Python mirror: the ★ arm on 5000 random pairs of 100-letter words
# over the letters a to c, all drawn first.


def count_substrings(s, t):
    a, b = s.encode(), t.encode()
    n, m = len(a), len(b)
    left = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            if a[i] == b[j]:
                left[i + 1][j + 1] = left[i][j] + 1
    right = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                right[i][j] = right[i + 1][j + 1] + 1
    count = 0
    for i in range(n):
        for j in range(m):
            if a[i] != b[j]:
                count += (left[i][j] + 1) * (right[i + 1][j + 1] + 1)
    return count


seed = 1638


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word():
    return "".join(chr(ord("a") + next_random() % 3) for _ in range(100))


def main():
    pairs = []
    for _ in range(5000):
        s = random_word()
        t = random_word()
        pairs.append((s, t))
    check = 0
    total = 0
    for s, t in pairs:
        count = count_substrings(s, t)
        total += count
        check = (check * 31 + count + 1) % 1000000007
    print(f"5000 pairs of 100 letters: counts sum to {total}, checksum {check}")


main()
