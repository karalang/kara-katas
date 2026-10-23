# LeetCode #890: Find and Replace Pattern -- Python mirror of the two-maps
# solution in find_and_replace_pattern.kara, with the same test harness.
#
# A word matches when some one-to-one renaming of letters turns the
# pattern into it. Walk the pattern and the word together, keeping the
# letter each pattern letter has become and the pattern letter each word
# letter came from; a clash with either map rules the word out. The
# words that match are kept in their order. O(total letters).


def find_and_replace_pattern(words, pattern):
    return [word for word in words if matches(word, pattern)]


def matches(word, pattern):
    to = {}
    frm = {}
    for p, w in zip(pattern, word):
        if p in to:
            if to[p] != w:
                return False
        else:
            to[p] = w
        if w in frm:
            if frm[w] != p:
                return False
        else:
            frm[w] = p
    return True


# ---- test harness ----------------------------------------------------------


def show(words, pattern):
    found = find_and_replace_pattern(words, pattern)
    print(f"words = [{', '.join(words)}], pattern = {pattern} -> [{', '.join(found)}]")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a random word of `length` letters from the first `letters` of the alphabet
def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


# the pattern with its letters renamed by a random one-to-one map, or, half
# the time, by one that sends two letters to the same one
def renamed(pattern):
    m = list(range(26))
    for i in range(1, 26):
        j = next_random() % (i + 1)
        m[i], m[j] = m[j], m[i]
    if next_random() % 2 == 0:
        a = next_random() % 26
        b = next_random() % 26
        m[a] = m[b]
    return "".join(chr(97 + m[ord(c) - 97]) for c in pattern)


def main():
    global seed
    show(["abc", "deq", "mee", "aqq", "dkd", "ccc"], "abb")
    show(["a", "b", "c"], "a")
    show(["ab", "ba", "aa", "bb", "zy"], "xy")
    show(["aa", "bb", "ab"], "cc")
    show(["abab", "baba", "abba", "cdcd", "ccdd"], "xyxy")
    show(["abcdefghijklmnopqrst", "bcdefghijklmnopqrsta", "aacdefghijklmnopqrst"], "tsrqponmlkjihgfedcba")
    # random cases of LeetCode's sizes: up to 50 words of up to 20
    # letters, from alphabets of 2 to 26 letters; half the words are the
    # pattern renamed
    seed = 890
    found = 0
    check = 0
    for _ in range(3000):
        length = 1 + next_random() % 20
        letters = 2 + next_random() % 25
        pattern = random_word(length, letters)
        count = 1 + next_random() % 50
        words = []
        for _ in range(count):
            if next_random() % 2 == 0:
                words.append(renamed(pattern))
            else:
                words.append(random_word(length, letters))
        kept = find_and_replace_pattern(words, pattern)
        found += len(kept)
        for w in kept:
            for b in w.encode():
                check = (check * 131 + b) % 1000000007
    print(f"3000 cases of up to 50 words of up to 20 letters: {found} match, checksum {check}")


main()
