# LeetCode #1239: Maximum Length of a Concatenated String with Unique
# Characters -- mirrors the ★ Kāra arm: each word with no repeated letter
# becomes a 26-bit mask, and a search over the words in order either skips
# a word or takes it when its mask is disjoint from the letters taken so
# far. The answer is the most bits ever set. O(2^n).


def mask_of(word):
    mask = 0
    for c in word:
        bit = 1 << (ord(c) - 97)
        if mask & bit:
            return None
        mask |= bit
    return mask


def search(masks, at, taken):
    if at == len(masks):
        return bin(taken).count("1")
    best = search(masks, at + 1, taken)
    if taken & masks[at] == 0:
        best = max(best, search(masks, at + 1, taken | masks[at]))
    return best


def max_length(arr):
    masks = [m for m in (mask_of(w) for w in arr) if m is not None]
    return search(masks, 0, 0)


# ---- test harness ----------------------------------------------------------

seed = 1239


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(count, longest, alphabet):
    words = []
    for _ in range(count):
        n = next_random() % longest + 1
        words.append("".join(chr(97 + next_random() % alphabet) for _ in range(n)))
    return words


def main():
    print(max_length(["un", "iq", "ue"]))
    print(max_length(["cha", "r", "act", "ers"]))
    print(max_length(["abcdefghijklmnopqrstuvwxyz"]))
    print(max_length(["aa", "bb"]))
    check = 0
    for _ in range(1000):
        count = next_random() % 16 + 1
        alphabet = next_random() % 19 + 8
        words = random_words(count, 6, alphabet)
        check = (check * 131 + max_length(words)) % 1000000007
    print(f"1000 random lists: checksum {check}")
    singles = [chr(97 + k) for k in range(16)]
    long = random_words(16, 4, 26)
    alphabets = ["abcdefghijklmnopqrstuvwxyz"] * 16
    print(f"16 words: {max_length(singles)}, {max_length(long)}, {max_length(alphabets)}")


main()
