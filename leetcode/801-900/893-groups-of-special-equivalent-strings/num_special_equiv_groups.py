# LeetCode #893: Groups of Special-Equivalent Strings -- Python mirror of
# the letter-count solution in num_special_equiv_groups.kara, with the
# same test harness.
#
# Swaps among the even positions can put their letters in any order, and
# likewise the odd ones, but no letter ever crosses from one set to the
# other. So two words are special-equivalent exactly when they hold the
# same letters at even positions and the same at odd positions. Write
# those 52 counts as a key, and count the different keys. O(total
# letters).


def num_special_equiv_groups(words):
    keys = set()
    for word in words:
        count = [0] * 52
        for i, ch in enumerate(word):
            count[ord(ch) - 97 + 26 * (i % 2)] += 1
        keys.add("".join(f"{c}," for c in count))
    return len(keys)


# ---- test harness ----------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(words):
    print(f"words = [{', '.join(words)}] -> {num_special_equiv_groups(words)}")


# a random word of `len` letters from the first `letters` of the alphabet
def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


# the word with random swaps among its even positions and among its odd
# ones, so it stays in the same group
def shuffled(word):
    b = list(word)
    n = len(b)
    for _ in range(n):
        i = next_random() % n
        j = next_random() % n
        if i % 2 == j % 2:
            b[i], b[j] = b[j], b[i]
    return "".join(b)


def main():
    global seed
    show(["abcd", "cdab", "cbad", "xyzz", "zzxy", "zzyx"])
    show(["abc", "acb", "bac", "bca", "cab", "cba"])
    show(["a", "b", "a"])
    show(["ab", "ba"])
    show(["abab", "baba", "aabb", "bbaa"])
    show(["abcdefghijklmnopqrst", "srqponmlkjihgfedcbat", "tsrqponmlkjihgfedcba"])
    # random cases of LeetCode's sizes: up to 1000 words of up to 20
    # letters from 2 to 26 letters; half the words are an earlier word
    # with its even and odd letters shuffled
    seed = 893
    words_in_all = 0
    groups = 0
    check = 0
    for _ in range(100):
        count = 1 + next_random() % 1000
        length = 1 + next_random() % 20
        letters = 2 + next_random() % 25
        words = []
        for _ in range(count):
            if len(words) > 0 and next_random() % 2 == 0:
                k = next_random() % len(words)
                words.append(shuffled(words[k]))
            else:
                words.append(random_word(length, letters))
        got = num_special_equiv_groups(words)
        words_in_all += count
        groups += got
        check = (check * 131 + got) % 1000000007
    print(f"100 cases of up to 1000 words of up to 20 letters ({words_in_all} words): {groups} groups, checksum {check}")


main()
