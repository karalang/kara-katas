# LeetCode #884 bench: Python mirror of uncommon_from_sentences.kara (the ★
# arm, one map of counts) on the same 1000 sentences.


def uncommon_from_sentences(s1, s2):
    counts = {}
    for word in s1.split(" "):
        counts[word] = counts.get(word, 0) + 1
    for word in s2.split(" "):
        counts[word] = counts.get(word, 0) + 1
    return [word for word, n in counts.items() if n == 1]


seed = 884


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# up to 200 characters, words of 1 to 4 of the letters a to e
def sentence():
    out = ""
    while True:
        size = next_random() % 4 + 1
        word = ""
        for _ in range(size):
            word += chr(97 + next_random() % 5)
        if len(out) == 0:
            out = word
        elif len(out) + 1 + len(word) <= 200:
            out = out + " " + word
        else:
            return out
        if next_random() % 80 == 0:
            return out


# the same for a word wherever it sits in the answer
def word_hash(word):
    h = 7
    for b in word.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    sentences = [sentence() for _ in range(1000)]
    total = 0
    check = 0
    for r in range(200):
        for i in range(1000):
            words = uncommon_from_sentences(sentences[i], sentences[(i + r + 1) % 1000])
            total += len(words)
            for w in words:
                check = (check + word_hash(w)) % 1000000007
    print(f"1000 sentences, each paired with 200 others: {total} uncommon words, checksum {check}")


main()
