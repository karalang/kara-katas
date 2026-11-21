# LeetCode #2414: Length of the Longest Alphabetical Continuous Substring
# -- the bench, the ★ arm in Python: one scan, the run growing while each
# letter follows the one before, the longest run kept.

seed = 2414


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def longest_continuous_substring(s):
    run = 1
    best = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1] + 1:
            run += 1
            best = max(best, run)
        else:
            run = 1
    return best


def main():
    strings = []
    for i in range(10):
        b = []
        for j in range(100000):
            if j > 0 and b[-1] < ord("z") and next_random() % (i + 2) != 0:
                b.append(b[-1] + 1)
            else:
                b.append(ord("a") + next_random() % 26)
        strings.append(bytes(b))
    check = 0
    for p in range(200):
        for s in strings:
            check = (check * 31 + longest_continuous_substring(s) + p) % 1000000007
    print(f"200 passes over 10 strings of 10^5 letters: checksum {check}")


main()
