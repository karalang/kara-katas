# LeetCode #1147: Longest Chunked Palindrome Decomposition -- the Python
# mirror of the ★ arm: greedy from both ends, the shortest equal chunks
# taken off, the middle one more.


def longest_decomposition(t):
    i, j, k = 0, len(t), 0
    while i < j:
        size = 1
        while 2 * size <= j - i and t[i:i + size] != t[j - size:j]:
            size += 1
        if 2 * size > j - i:
            return k + 1
        k += 2
        i += size
        j -= size
    return k


seed = 1147


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def text():
    size = 1 + next_random() % 4
    unit = [chr(97 + next_random() % 2) for _ in range(size)]
    b = [unit[i % size] for i in range(1000)]
    at = next_random() % 1000
    b[at] = chr(97 + next_random() % 2)
    return "".join(b)


def main():
    texts = [text() for _ in range(20)]
    total = check = 0
    for r in range(20000):
        texts[r % 20] = text()
        for t in texts:
            k = longest_decomposition(t)
            total += k
            check = (check * 31 + k) % 1000000007
    print(f"20000 rounds over 20 texts of 1000 letters: chunks total {total}, checksum {check}")


main()
