# LeetCode #2273: Find Resultant Array After Removing Anagrams -- the
# Python mirror of the ★ arm, `anagrams.kara`, line for line. Its output
# is byte-identical.


def sorted_letters(word):
    return "".join(sorted(word))


def remove_anagrams(words):
    kept = []
    last = ""
    for w in words:
        key = sorted_letters(w)
        if not kept or key != last:
            kept.append(w)
        last = key
    return kept


seed = 2273


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(m, long, k):
    words = []
    for i in range(m):
        if i > 0 and next_random() % 2 == 0:
            letters = list(words[i - 1])
            for j in range(len(letters) - 1, 0, -1):
                r = next_random() % (j + 1)
                letters[j], letters[r] = letters[r], letters[j]
            words.append("".join(letters))
        else:
            length = next_random() % long + 1
            words.append("".join(chr(97 + next_random() % k) for _ in range(length)))
    return words


def digest(words):
    h = len(words)
    for w in words:
        for b in w.encode():
            h = (h * 131 + b) % 1000000007
        h = (h * 131 + 7) % 1000000007
    return h


def show(words):
    return "[" + ", ".join(words) + "]"


def main():
    examples = [
        ["abba", "baba", "bbaa", "cd", "cd"],
        ["a", "b", "c", "d", "e"],
        ["z"],
        ["abc", "bca", "cab", "acb"],
        ["ab", "cd", "ba", "dc"],
        ["ab", "aab", "ba"],
        ["xy", "yx", "z", "z", "xy", "yx"],
    ]
    for words in examples:
        print(f"{show(words)} -> {show(remove_anagrams(words))}")
    kept = 0
    check = 0
    for t in range(3000):
        m = next_random() % 30 + 1
        words = random_words(m, [1, 3, 10][t % 3], [2, 3, 26][t // 3 % 3])
        left = remove_anagrams(words)
        kept += len(left)
        check = (check * 31 + digest(left)) % 1000000007
    print(f"3000 lists: {kept} words kept, checksum {check}")
    rand = random_words(100, 10, 26)
    family = ["abcdefghij" if i % 2 == 0 else "jihgfedcba" for i in range(100)]
    pairs = ["aabbccddee" if i % 4 < 2 else "zzyyxxwwvv" for i in range(100)]
    answers = [len(remove_anagrams(rand)), len(remove_anagrams(family)), len(remove_anagrams(pairs))]
    print(f"100 words: [{', '.join(map(str, answers))}] kept")


main()
