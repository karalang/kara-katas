# LeetCode #1065: Index Pairs of a String -- the benchmark, the same
# every-start-against-every-word search as index_pairs.kara.
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


def index_pairs(text, words):
    pairs = []
    for i in range(len(text)):
        for w in words:
            if text.startswith(w, i):
                pairs.append((i, i + len(w) - 1))
    pairs.sort()
    return pairs


def main():
    # 40 texts of 20000 letters over 2 to 4, each with up to 100 words of 1
    # to 12 letters, built once, then each answered
    texts = []
    lists = []
    for t in range(40):
        k = 2 + t % 3
        text = random_word(20000, k)
        lists.append(random_words(text, 100, 12, k))
        texts.append(text)
    calls = count = check = 0
    for t in range(40):
        pairs = index_pairs(texts[t], lists[t])
        count += len(pairs)
        for i, j in pairs:
            check = (check * 31 + i * 101 + j + 1) % 1000000007
        calls += 1
    print(f"{calls} calls: {count} pairs, checksum {check}")


main()
