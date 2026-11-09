# LeetCode #1078: Occurrences After Bigram -- the Python mirror of the
# ★ arm (occurrences.kara): same algorithm, same harness, same output.


def find_occurrences(text, first, second):
    words = text.split(" ")
    out = []
    for i in range(2, len(words)):
        if words[i - 2] == first and words[i - 1] == second:
            out.append(words[i])
    return out


seed = 1078


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(longest, k):
    n = next_random() % longest + 1
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def random_problem(size, longest, k, limit):
    vocabulary = [random_word(longest, k) for _ in range(size)]
    words = []
    length = -1
    target = next_random() % limit + 1
    while True:
        w = vocabulary[next_random() % size]
        if words and length + 1 + len(w) > target:
            break
        length += 1 + len(w)
        words.append(w)

    def pick():
        if next_random() % 3 < 2:
            return words[next_random() % len(words)]
        return vocabulary[next_random() % size]

    first = pick()
    second = pick()
    return " ".join(words), first, second


def checksum(words):
    check = len(words)
    for w in words:
        for c in w.encode():
            check = (check * 31 + c) % 1000000007
        check = (check * 31 + 32) % 1000000007
    return check


def show(words):
    return "[" + ", ".join(words) + "]"


def main():
    examples = [
        ("alice is a good girl she is a good student", "a", "good"),
        ("we will we will rock you", "we", "will"),
        ("a a a a", "a", "a"),
        ("a b", "a", "b"),
        ("a b c", "a", "b"),
        ("x y z x y", "x", "y"),
        ("ab abc ab abc abd", "ab", "abc"),
        ("jkypmsxd jkypmsxd kcyxdfnoa jkypmsxd kcyxdfnoa jkypmsxd kcyxdfnoa kcyxdfnoa jkypmsxd kcyxdfnoa", "kcyxdfnoa", "jkypmsxd"),
        ("one two three", "two", "three"),
        ("aa a aa a aa", "a", "aa"),
    ]
    for text, first, second in examples:
        print(f'"{text}" {first} {second} -> {show(find_occurrences(text, first, second))}')
    found = letters = check = 0
    for _ in range(3000):
        size = next_random() % 4 + 1
        text, first, second = random_problem(size, 2, 2, 40)
        out = find_occurrences(text, first, second)
        found += len(out)
        letters += sum(len(w) for w in out)
        check = (check * 31 + checksum(out)) % 1000000007
    print(f"3000 texts up to 40 characters: {found} words found, {letters} letters, checksum {check}")
    found = letters = check = 0
    for _ in range(1000):
        k = next_random() % 3 + 1
        size = next_random() % 12 + 1
        text, first, second = random_problem(size, 10, k, 1000)
        out = find_occurrences(text, first, second)
        found += len(out)
        letters += sum(len(w) for w in out)
        check = (check * 31 + checksum(out)) % 1000000007
    print(f"1000 texts up to 1000 characters: {found} words found, {letters} letters, checksum {check}")
    a500 = " ".join(["a"] * 500)
    print(f"500 a's after a a: {len(find_occurrences(a500, 'a', 'a'))}")
    ab = " ".join(["ab c"] * 200) + " ab"
    print(f"ab c 200 times after c ab: {len(find_occurrences(ab, 'c', 'ab'))}, after ab c: {len(find_occurrences(ab, 'ab', 'c'))}")


main()
