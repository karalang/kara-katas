# LeetCode #691: Stickers to Spell Word -- a table over the subsets of the target.
#
# A mirror of stickers_to_spell_word.kara (the ★ arm) and its harness.


def min_stickers(stickers, target):
    t = target.encode()
    m = len(t)
    full = (1 << m) - 1
    counts = []
    for s in stickers:
        c = [0] * 26
        for b in s.encode():
            c[b - 97] += 1
        counts.append(c)
    dp = [-1] * (full + 1)
    dp[0] = 0
    left = [0] * 26
    for mask in range(full + 1):
        if dp[mask] < 0:
            continue
        for c in counts:
            for k in range(26):
                left[k] = c[k]
            nxt = mask
            for i in range(m):
                k = t[i] - 97
                if nxt & (1 << i) == 0 and left[k] > 0:
                    left[k] -= 1
                    nxt = nxt | (1 << i)
            if nxt != mask and (dp[nxt] < 0 or dp[mask] + 1 < dp[nxt]):
                dp[nxt] = dp[mask] + 1
    return dp[full]


# ---- harness ----------------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, alphabet):
    return "".join(chr(97 + next_random() % alphabet) for _ in range(length))


def main():
    global seed
    ex1 = min_stickers(["with", "example", "science"], "thehat")
    ex2 = min_stickers(["notice", "possible"], "basicbasic")
    print(f"example 1: {ex1}")
    print(f"example 2: {ex2}")
    itself = min_stickers(["target"], "target")
    missing = min_stickers(["abc", "def"], "abz")
    print(f"the target itself: {itself}")
    print(f"a missing letter: {missing}")
    fifteen = "a" * 15
    from_two = min_stickers(["aa"], fifteen)
    from_one_five = min_stickers(["a", "aaaaa"], fifteen)
    print(f"15 a's: from aa {from_two}, from a and aaaaa {from_one_five}")
    singles = [chr(97 + k) for k in range(26)]
    pangram = "thequickbrownfx"
    one_each = min_stickers(singles, pangram)
    singles.append("xfnworbkciuqeht")
    print(f"15 different letters: from 26 singles {one_each}, with the whole word added {min_stickers(singles, pangram)}")

    seed = 691
    big = [random_word(10, 12) for _ in range(50)]
    big_target = random_word(15, 12)
    print(f"50 stickers of 10, a target of 15: {min_stickers(big, big_target)}")

    checksum = 0
    impossible = 0
    for _ in range(300):
        alphabet = 2 + next_random() % 25
        n = 1 + next_random() % 30
        stickers = []
        for _ in range(n):
            length = 1 + next_random() % 10
            stickers.append(random_word(length, alphabet))
        target = random_word(1 + next_random() % 12, alphabet)
        r = min_stickers(stickers, target)
        if r < 0:
            impossible += 1
        checksum = (checksum * 31 + r + 2) % 1000000007
    print(f"300 random problems: {impossible} impossible, checksum {checksum}")


main()
