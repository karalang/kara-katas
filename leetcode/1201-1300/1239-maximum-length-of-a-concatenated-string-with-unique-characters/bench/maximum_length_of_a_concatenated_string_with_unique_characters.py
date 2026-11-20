# LeetCode #1239: the benchmark, mirroring the Kāra file.

seed = 1239


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    lists = []
    for _ in range(20000):
        words = []
        for _ in range(16):
            n = next_random() % 2 + 1
            words.append("".join(chr(97 + next_random() % 26) for _ in range(n)))
        lists.append(words)
    total = 0
    check = 0
    for words in lists:
        best = max_length(words)
        total += best
        check = (check * 131 + best) % 1000000007
    print(f"20000 lists of 16 words: total {total}, checksum {check}")


main()
