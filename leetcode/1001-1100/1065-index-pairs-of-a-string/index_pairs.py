# LeetCode #1065: Index Pairs of a String -- the Python mirror of
# index_pairs.kara (the ★ arm): every start against every word, then the
# pairs sorted.


def index_pairs(text, words):
    pairs = []
    for i in range(len(text)):
        for w in words:
            if text.startswith(w, i):
                pairs.append((i, i + len(w) - 1))
    pairs.sort()
    return pairs


seed = 1065


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def random_words(text, count, longest, k):
    words = []
    for w in range(count):
        n = next_random() % longest + 1
        if w % 2 == 1 and n <= len(text):
            at = next_random() % (len(text) - n + 1)
            word = text[at : at + n]
        else:
            word = random_word(n, k)
        if word not in words:
            words.append(word)
    return words


def checksum(pairs):
    check = 0
    for i, j in pairs:
        check = (check * 31 + i * 101 + j + 1) % 1000000007
    return check


def show_words(words):
    return "[" + ", ".join(words) + "]"


def show_pairs(pairs):
    return "[" + ", ".join(f"({i}, {j})" for i, j in pairs) + "]"


def main():
    examples = [
        ("thestoryofleetcodeandme", ["story", "fleet", "leetcode"]),
        ("ababa", ["aba", "ab"]),
        ("a", ["a"]),
        ("abc", ["d", "abcd"]),
        ("aaaa", ["a", "aa", "aaa"]),
        ("xyz", ["y", "xyz"]),
        ("mississippi", ["issi", "ss", "i", "pp"]),
    ]
    for text, words in examples:
        print(f"{text} {show_words(words)} -> {show_pairs(index_pairs(text, words))}")
    count = check = 0
    for _ in range(3000):
        k = next_random() % 3 + 1
        text = random_word(next_random() % 20 + 1, k)
        words = random_words(text, next_random() % 5 + 1, 4, k)
        pairs = index_pairs(text, words)
        count += len(pairs)
        check = (check * 31 + checksum(pairs)) % 1000000007
    print(f"3000 texts of 1 to 20 letters: {count} pairs, checksum {check}")
    count = check = 0
    for _ in range(300):
        k = next_random() % 25 + 2
        text = random_word(next_random() % 51 + 50, k)
        words = random_words(text, next_random() % 20 + 1, 8, k)
        pairs = index_pairs(text, words)
        count += len(pairs)
        check = (check * 31 + checksum(pairs)) % 1000000007
    print(f"300 texts of 50 to 100 letters: {count} pairs, checksum {check}")
    a = "a" * 100
    pairs = index_pairs(a, [a[:n] for n in range(1, 21)])
    print(f"100 a's, 20 runs: {len(pairs)} pairs, checksum {checksum(pairs)}")
    ab = "".join("a" if i % 2 == 0 else "b" for i in range(100))
    pairs = index_pairs(ab, ["ab", "ba", "aba", "bab"])
    print(f"100 alternating, 4 words: {len(pairs)} pairs, checksum {checksum(pairs)}")


main()
