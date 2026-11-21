# LeetCode #2430: Maximum Deletions on a String -- the Python mirror of
# the ★ arm: best[i] from the back over two rows of common prefixes.

seed = 2430


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def delete_string(s):
    b = s.encode()
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


def random_word(n, kinds, stay):
    out = []
    for i in range(n):
        back = 1 + next_random() % 3
        if i >= back and next_random() % stay == 0:
            out.append(out[i - back])
        else:
            out.append(chr(ord("a") + next_random() % kinds))
    return "".join(out)


def main():
    for s in ["abcabcdabc", "aaabaab", "aaaaa", "a", "ab"]:
        print(f"{s}: {delete_string(s)}")
    print(f"a * 1000: {delete_string('a' * 1000)}")
    print(f"ab * 500: {delete_string('ab' * 500)}")
    print(f"aab * 333: {delete_string('aab' * 333)}")
    x = delete_string(random_word(1000, 2, 2))
    y = delete_string(random_word(1000, 26, 2))
    print(f"{x} {y}")
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 14
        kinds = 1 + next_random() % 3
        answer = delete_string(random_word(n, kinds, 1 + next_random() % 3))
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
