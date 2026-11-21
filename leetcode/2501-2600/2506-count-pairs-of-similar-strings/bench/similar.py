# LeetCode #2506: Count Pairs Of Similar Strings -- benchmark mirror of
# the ★ arm (similar.kara): 1000 lists of 100 words built once, then the
# passes; each copies one word of every list over another, chosen by the
# checksum so far, asks, and puts the word back.


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


def random_word():
    # 1 to 100 letters from the first 3 to 6 of the alphabet
    length = next_random() % 100 + 1
    letters = next_random() % 4 + 3
    return "".join(chr(ord('a') + next_random() % letters) for _ in range(length))


def main():
    passes = 24
    lists = [[random_word() for _ in range(100)] for _ in range(1000)]
    check = 0
    for p in range(passes):
        for words in lists:
            at = check % 100
            was = words[at]
            words[at] = words[(check // 100 + p) % 100]
            check = (check * 31 + similar_pairs(words) + p) % 1000000007
            words[at] = was
    print(f"{passes} passes over 1000 lists of 100 words: checksum {check}")


main()
