# LeetCode #2430: Maximum Deletions on a String -- the bench, the ★ arm:
# the longest common prefix of the suffixes at `i` and `k` kept in two
# rows, each row from the one after it, and `best[i]` the most
# operations that clear the suffix from `i`.


def delete_string(b):
    n = len(b)
    next_row = [0] * (n + 1)
    row = [0] * (n + 1)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        for k in range(i + 1, n):
            row[k] = next_row[k + 1] + 1 if b[i] == b[k] else 0
        best[i] = 1
        for j in range(1, (n - i) // 2 + 1):
            if row[i + j] >= j:
                best[i] = max(best[i], best[i + j] + 1)
        next_row, row = row, next_row
    return best[0]


seed = 2430


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    words = []
    for _ in range(8):
        w = []
        for i in range(4000):
            back = 1 + next_random() % 3
            if i >= back and next_random() % 2 == 0:
                w.append(w[i - back])
            else:
                w.append(97 + next_random() % 2)
        words.append(w)
    check = 0
    for p in range(6):
        for w in range(len(words)):
            at = (p * 997 + w * 131) % 4000
            words[w][at] = 97 + p % 2
            check = (check * 31 + delete_string(words[w]) + p) % 1000000007
    print(f"6 passes over 8 words of 4000 letters: checksum {check}")


main()
