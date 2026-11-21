# LeetCode #2506: Count Pairs Of Similar Strings -- mirror of the ★ arm
# (similar.kara): every word's letters as a 26-bit mask, and each word
# pairs with every earlier word of the same mask, counted in a dict.


def similar_pairs(words):
    seen = {}
    pairs = 0
    for word in words:
        mask = 0
        for ch in word:
            mask |= 1 << (ord(ch) - ord('a'))
        pairs += seen.get(mask, 0)
        seen[mask] = seen.get(mask, 0) + 1
    return pairs


seed = 2506


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(ord('a') + next_random() % letters) for _ in range(length))


def main():
    cases = [
        ["aba", "aabb", "abcd", "bac", "aabc"],
        ["aabb", "ab", "ba"],
        ["nba", "cba", "dba"],
        ["z"],
        ["abc", "cab", "bca", "cba"],
        ["a", "aa", "aaa", "b", "bb"],
        ["abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "a"],
        ["ab", "abc", "abcd", "dcba", "cba"],
    ]
    for words in cases:
        print(f"{len(words)} words -> {similar_pairs(words)}")
    for letters in [3, 26]:
        check = 0
        none = 0
        for _ in range(2000):
            count = next_random() % 30 + 1
            words = [random_word(next_random() % 8 + 1, letters) for _ in range(count)]
            a = similar_pairs(words)
            if a == 0:
                none += 1
            check = (check * 31 + a) % 1000000007
        print(f"2000 random of {letters} letters: {none} with no pair, checksum {check}")
    same = ["".join(chr(ord('a') + (i + j) % 26) for j in range(100)) for i in range(100)]
    print(f"100 words of every letter -> {similar_pairs(same)}")
    long_words = [random_word(100, 26) for _ in range(100)]
    print(f"100 random words of 100 letters -> {similar_pairs(long_words)}")
    short_words = [random_word(next_random() % 4 + 1, 3) for _ in range(100)]
    print(f"100 random words to 4 letters from 3 -> {similar_pairs(short_words)}")

main()
