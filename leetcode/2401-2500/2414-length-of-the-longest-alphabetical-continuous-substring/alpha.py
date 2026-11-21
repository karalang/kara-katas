# LeetCode #2414: Length of the Longest Alphabetical Continuous Substring
# -- the mirror of the ★ arm: a run grows while each letter follows the
# one before it, and the longest run is the answer.

seed = 2414


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def longest_continuous_substring(s):
    run = 1
    best = 1
    for i in range(1, len(s)):
        if ord(s[i]) == ord(s[i - 1]) + 1:
            run += 1
            best = max(best, run)
        else:
            run = 1
    return best


def letters(n, kinds, step):
    out = []
    for i in range(n):
        if i > 0 and out[i - 1] < 122 and next_random() % step == 0:
            out.append(out[i - 1] + 1)
        else:
            out.append(97 + next_random() % kinds)
    return bytes(out).decode()


def main():
    print(longest_continuous_substring("abacaba"))
    print(longest_continuous_substring("abcde"))
    print(longest_continuous_substring("z"))
    print(f"{longest_continuous_substring('abcdefghijklmnopqrstuvwxyz')} {longest_continuous_substring('zyxwvutsrqponmlkjihgfedcba')}")
    print(longest_continuous_substring("xyzabcdefghijklmnopqrstuvwxyzab"))
    print(longest_continuous_substring(letters(100000, 26, 2)))
    print(longest_continuous_substring(letters(100000, 26, 100)))
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        kinds = 2 + next_random() % 25
        a = longest_continuous_substring(letters(n, kinds, 1 + next_random() % 4))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
