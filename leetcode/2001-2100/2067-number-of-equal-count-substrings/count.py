# LeetCode #2067: Number of Equal Count Substrings -- the Python mirror of
# count.kara (the ★ arm): for each number of different letters k, a window
# of length k * count slid over the text, counting the letters at exactly
# `count`.


def equal_count_substrings(s, count):
    b = s.encode()
    n = len(b)
    total = 0
    for k in range(1, 27):
        length = k * count
        if length > n:
            break
        seen = [0] * 26
        exact = 0
        for i in range(n):
            c = b[i] - 97
            seen[c] += 1
            if seen[c] == count:
                exact += 1
            elif seen[c] == count + 1:
                exact -= 1
            if i >= length:
                d = b[i - length] - 97
                if seen[d] == count:
                    exact -= 1
                seen[d] -= 1
                if seen[d] == count:
                    exact += 1
            if i + 1 >= length and exact == k:
                total += 1
    return total


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def text_of(n, k, count, p, seed):
    letters = "abcdefghijklmnopqrstuvwxyz"
    out = []
    length = 0
    while length < n:
        c = letters[next_random(seed) % k]
        run = count if next_random(seed) % 100 < p else 1
        out.append(c * min(run, n - length))
        length += min(run, n - length)
    return "".join(out)


def main():
    examples = [("aaabcbbcc", 3), ("abcd", 2), ("a", 5), ("a", 1), ("abcabc", 2), ("aabbccab", 2), ("zzzz", 2), ("abab", 1)]
    for s, count in examples:
        print(f"{s} {count} -> {equal_count_substrings(s, count)}")
    seed = [2067]
    total = 0
    check = 0
    for _ in range(500):
        n = next_random(seed) % 300 + 1
        k = next_random(seed) % 26 + 1
        count = next_random(seed) % 10 + 1
        p = next_random(seed) % 101
        a = equal_count_substrings(text_of(n, k, count, p, seed), count)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"500 texts: sum {total}, checksum {check}")
    print(f"30000 letters, 4 kinds, 5 -> {equal_count_substrings(text_of(30000, 4, 5, 50, seed), 5)}")
    print(f"30000 letters, 26 kinds, 3 -> {equal_count_substrings(text_of(30000, 26, 3, 100, seed), 3)}")


main()
