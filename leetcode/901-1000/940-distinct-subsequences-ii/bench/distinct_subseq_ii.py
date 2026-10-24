# Benchmark: LeetCode #940 Distinct Subsequences II -- the ★ arm,
# doubling less the repeats, on 100 words of 2000 letters, LeetCode's
# longest, in 200 rounds. Mirrors distinct_subseq_ii.kara, .c, .rs and
# go-seq/.


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


seed = 940


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 200
    count = 100
    words = []
    for _ in range(count):
        k = 1 + next_random() % 26
        words.append("".join(chr(next_random() % k + 97) for _ in range(2000)))
    total = check = 0
    for r in range(rounds):
        for i in range(count):
            a = distinct_subseq_ii(words[(r + i) % count])
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over {count} words of 2000 letters: counts adding to {total}, checksum {check}")


main()
