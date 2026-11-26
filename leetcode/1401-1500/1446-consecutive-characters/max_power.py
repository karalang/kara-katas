# LeetCode #1446 Consecutive Characters: a mirror of max_power.kara.


def max_power(s):
    # the length of the run the letter so far ends, and the longest run
    best = 0
    run = 0
    last = " "
    for ch in s:
        if ch == last:
            run += 1
        else:
            run = 1
            last = ch
        best = max(best, run)
    return best


# ---- test harness ---------------------------------------------------------

seed = 1446


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def main():
    cases = ["leetcode", "abbcccddddeeeeedcba", "a", "zzzzz", "ab", "aabbb", "abba"]
    print(" ".join(str(max_power(s)) for s in cases))
    same = "a" * 500
    turns = "ab" * 250
    two = drawn(500, 2)
    print(f"500 letters: {max_power(same)} {max_power(turns)} {max_power(two)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        k = 1 + next_random() % 26
        got = max_power(drawn(n, k))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random strings: {total} in all, checksum {check}")


main()
