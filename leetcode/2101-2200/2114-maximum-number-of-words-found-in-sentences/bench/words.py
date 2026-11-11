# LeetCode #2114: Maximum Number of Words Found in Sentences -- the
# benchmark, the same algorithm as words.kara: each sentence's spaces
# counted, plus one, and the largest taken.


def most_words_found(sentences):
    most = 0
    for s in sentences:
        most = max(most, s.count(" ") + 1)
    return most


seed = 2114


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(200):
        sentences = []
        for _ in range(100):
            words = next_random() % 25 + 1
            parts = []
            for w in range(words):
                n = next_random() % 6 + 1
                parts.append("".join(chr(97 + next_random() % 26) for _ in range(n)))
            sentences.append(" ".join(parts))
        lists.append(sentences)
    total = 0
    check = 0
    for rnd in range(10):
        for a in range(200):
            j = (rnd * 37 + a) % 100
            lists[a][j] += " a"
            got = most_words_found(lists[a])
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"2000 solves: {total} words, checksum {check}")


main()
