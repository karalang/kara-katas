# LeetCode #395: Longest Substring with At Least K Repeating Characters
# -- Python mirror of longest_substring.kara (divide and conquer).


def longest(b, lo, hi, k):
    if hi - lo < k:
        return 0
    count = [0] * 26
    for i in range(lo, hi):
        count[b[i] - 97] += 1
    best = 0
    start = lo
    split = False
    for i in range(lo, hi):
        if count[b[i] - 97] < k:
            split = True
            best = max(best, longest(b, start, i, k))
            start = i + 1
    if not split:
        return hi - lo
    return max(best, longest(b, start, hi, k))


def longest_substring(s, k):
    b = s.encode()
    return longest(b, 0, len(b), k)


seed = 395


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s, k):
    print(f's = "{s}", k = {k}: {longest_substring(s, k)}')


def main():
    show("aaabb", 3)
    show("ababbc", 2)
    show("a", 1)
    show("a", 2)
    show("abcde", 1)
    show("abcde", 2)
    show("aaabbbcdd", 3)
    show("bbaaacbd", 3)
    show("weitong", 2)
    show("aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz", 2)
    show("aaaaaaaaaab", 2)
    total = 0
    checksum = 0
    for _ in range(3000):
        n = 1 + step() % 40
        s = "".join(chr(step() % 4 + 97) for _ in range(n))
        k = 1 + step() % 5
        r = longest_substring(s, k)
        total += r
        checksum = (checksum * 41 + r) % 1000000007
    print(f"3000 random strings: total {total}, checksum {checksum}")


main()
