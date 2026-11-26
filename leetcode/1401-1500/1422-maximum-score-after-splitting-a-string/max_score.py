# LeetCode #1422, Python mirror of max_score.kara: a split scores the ones
# in all of s, plus the zeros less the ones to its left, and the best is
# the most that difference reaches over the splits.


def max_score(s):
    ones = s.count("1")
    lead = 0
    best = None
    for d in s[:-1]:
        lead += 1 if d == "0" else -1
        best = lead if best is None else max(best, lead)
    return ones + best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, ones):
    return "".join("1" if next_random() % 10 < ones else "0" for _ in range(n))


def main():
    global seed
    cases = ["011101", "00111", "1111", "00", "01", "10", "11", "0101"]
    print(" ".join(str(max_score(s)) for s in cases))
    seed = 1422
    drawn_most = drawn(500, 5)
    print(f"500 digits: {max_score('0' * 500)} {max_score('1' * 500)} {max_score(drawn_most)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 2 + next_random() % 59
        ones = next_random() % 11
        got = max_score(drawn(n, ones))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random strings: {total} in all, checksum {check}")


main()
