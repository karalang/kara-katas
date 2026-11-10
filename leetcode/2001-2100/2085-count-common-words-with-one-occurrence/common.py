# LeetCode #2085: Count Common Words With One Occurrence -- Python mirror
# of the ★ arm (common.kara): each list's words counted, and the words
# once in each counted.


def counts(words):
    seen = {}
    for w in words:
        seen[w] = seen.get(w, 0) + 1
    return seen


def count_words(words1, words2):
    one = counts(words1)
    two = counts(words2)
    return sum(1 for w, c in one.items() if c == 1 and two.get(w) == 1)


seed = 2085


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(width, longest):
    letters = "abcdefghijklmnopqrstuvwxyz"
    n = next_random() % longest + 1
    return "".join(letters[next_random() % width] for _ in range(n))


def main():
    examples = [
        ("leetcode is amazing as is", "amazing leetcode is"),
        ("b bb bbb", "a aa aaa"),
        ("a ab", "a a a ab"),
        ("x", "x"),
        ("x x", "x"),
        ("one two three", "three two one"),
        ("a b c d", "d d c b b a"),
    ]
    for one, two in examples:
        print(f"[{one}] [{two}] -> {count_words(one.split(' '), two.split(' '))}")
    total = 0
    check = 0
    for _ in range(300):
        width = [2, 3, 5][next_random() % 3]
        n1 = next_random() % 100 + 1
        n2 = next_random() % 100 + 1
        words1 = [random_word(width, 3) for _ in range(n1)]
        words2 = [random_word(width, 3) for _ in range(n2)]
        a = count_words(words1, words2)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"300 pairs: sum {total}, checksum {check}")
    vocabulary = [random_word(3, 30) for _ in range(1500)]
    words1 = [vocabulary[next_random() % 1500] for _ in range(1000)]
    words2 = [vocabulary[next_random() % 1500] for _ in range(1000)]
    print(f"1000 words a side: {count_words(words1, words2)}")


main()
