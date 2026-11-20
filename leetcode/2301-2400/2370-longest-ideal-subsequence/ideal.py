# LeetCode #2370: Longest Ideal Subsequence -- the Python mirror of the ★
# arm: best[c] is the longest ideal subsequence so far that ends in letter
# c, and a new letter extends the best one within k letters of it.


def longest_ideal_string(s, k):
    best = [0] * 26
    for b in s.encode():
        c = b - ord("a")
        lo = max(c - k, 0)
        hi = min(c + k, 25)
        best[c] = max(best[lo:hi + 1]) + 1
    return max(best)


SEED = [2370]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def letters(codes):
    return "".join(chr(c + 97) for c in codes)


def main():
    # LeetCode's two examples; one letter; 10^5 letters running through
    # the alphabet again and again, with k of 0, 1 and 25; 10^5 letters
    # a and z in turn, with k of 24 and 25; then 2000 random strings of 1
    # to 40 letters from the first 1 to 26 of the alphabet, with k of 0
    # to 25
    print(longest_ideal_string("acfgbd", 2))
    print(longest_ideal_string("abcd", 3))
    print(longest_ideal_string("z", 0))
    cycle = letters([i % 26 for i in range(100000)])
    print(f"{longest_ideal_string(cycle, 0)} {longest_ideal_string(cycle, 1)} {longest_ideal_string(cycle, 25)}")
    ends = letters([(i % 2) * 25 for i in range(100000)])
    print(f"{longest_ideal_string(ends, 24)} {longest_ideal_string(ends, 25)}")
    check = 0
    whole = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        top = 1 + next_random() % 26
        k = next_random() % 26
        s = letters([next_random() % top for _ in range(n)])
        t = longest_ideal_string(s, k)
        check = (check * 31 + t) % 1000000007
        if t == n:
            whole += 1
    print(f"2000 strings: checksum {check}, {whole} ideal whole")


main()
