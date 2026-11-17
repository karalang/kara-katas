# LeetCode #2255: Count Prefixes of a Given String -- Python mirror of
# prefixes.kara: each word tested with s.startswith(word), the ones that
# hold counted.


def count_prefixes(words, s):
    return sum(1 for w in words if s.startswith(w))


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(longest, letters):
    length = next_random() % longest + 1
    return "".join("abcde"[next_random() % letters] for _ in range(length))


def main():
    global seed
    examples = [
        (["a", "b", "c", "ab", "bc", "abc"], "abc"),
        (["a", "a"], "aa"),
        (["abcd", "abc"], "abc"),
        (["z"], "z"),
        (["ab", "ab", "ab", "b"], "abab"),
        (["abd", "abc", "ab", "abcde"], "abcd"),
    ]
    for words, s in examples:
        print(f"[{', '.join(words)}] {s} -> {count_prefixes(words, s)}")
    seed = 2255
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 8 + 1
        words = [random_word(4, 2) for _ in range(n)]
        s = random_word(6, 2)
        count = count_prefixes(words, s)
        total += count
        check = (check * 31 + count + 1) % 1000000007
    print(f"2000 cases: {total} prefixes in all, checksum {check}")
    total = 0
    check = 0
    for c in range(200):
        letters = c % 5 + 1
        words = [random_word(10, letters) for _ in range(1000)]
        s = random_word(10, letters)
        count = count_prefixes(words, s)
        total += count
        check = (check * 31 + count + 1) % 1000000007
    print(f"200 cases of 1000 words: {total} prefixes in all, checksum {check}")


main()
