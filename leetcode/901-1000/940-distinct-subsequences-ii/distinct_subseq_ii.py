# LeetCode #940: Distinct Subsequences II -- doubling, less the repeats.
# Mirrors distinct_subseq_ii.kara (the ★ arm) and prints the same output.


def distinct_subseq_ii(s):
    m = 1000000007
    n = len(s)
    count = [1]
    last = [0] * 26
    for i in range(n):
        c = ord(s[i]) - 97
        nxt = 2 * count[i] % m
        if last[c] > 0:
            nxt = (nxt - count[last[c] - 1] + m) % m
        count.append(nxt)
        last[c] = i + 1
    return (count[n] - 1 + m) % m


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return "".join(chr(next_random() % k + 97) for _ in range(n))


def main():
    global seed
    for s in ["abc", "aba", "aaa", "a", "ab", "abab", "zyxz", "abcdefghijklmnopqrstuvwxyz"]:
        print(f'"{s}": {distinct_subseq_ii(s)}')
    seed = 940
    letters = total = check = 0
    for _ in range(300):
        n = 1 + next_random() % 100
        k = 1 + next_random() % 26
        a = distinct_subseq_ii(random_word(n, k))
        letters += n
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"300 random words of {letters} letters: counts adding to {total}, checksum {check}")
    print(f"2000 times a: {distinct_subseq_ii('a' * 2000)}")
    print(f"ab 1000 times: {distinct_subseq_ii('ab' * 1000)}")
    print(f"the alphabet 76 times and abcd: {distinct_subseq_ii('abcdefghijklmnopqrstuvwxyz' * 76 + 'abcd')}")
    print(f"2000 random letters: {distinct_subseq_ii(random_word(2000, 26))}")
    print(f"2000 random letters from abc: {distinct_subseq_ii(random_word(2000, 3))}")


main()
