# LeetCode #1078 bench, Python mirror of occurrences.kara: the same texts,
# bigrams, rounds and checksum.


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


def main():
    rounds = 300
    vocabulary = [random_word(4, 3) for _ in range(12)]
    texts, firsts, seconds, owner = [], [], [], []
    for t in range(100):
        words = []
        length = -1
        while True:
            w = vocabulary[next_random() % 12]
            if length + 1 + len(w) > 1000:
                break
            length += 1 + len(w)
            words.append(w)
        for _ in range(8):
            if next_random() % 4 < 3:
                at = next_random() % (len(words) - 1)
                firsts.append(words[at])
                seconds.append(words[at + 1])
            else:
                firsts.append(vocabulary[next_random() % 12])
                seconds.append(vocabulary[next_random() % 12])
            owner.append(t)
        texts.append(" ".join(words))
    queries = len(firsts)
    found = 0
    check = 0
    for r in range(rounds):
        for j in range(queries):
            q = (j * 7 + r) % queries
            out = find_occurrences(texts[owner[q]], firsts[q], seconds[q])
            found += len(out)
            for w in out:
                for c in w.encode():
                    check = (check * 31 + c) % 1000000007
            check = (check * 31 + len(out)) % 1000000007
    print(f"{rounds} rounds of {queries} bigrams over 100 texts: {found} words found, checksum {check}")


main()
