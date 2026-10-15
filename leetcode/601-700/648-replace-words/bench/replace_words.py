# LeetCode #648: Replace Words -- Python mirror of the Kāra bench.
#
# The ★ arm over the same inputs and rounds: a trie of the roots as a
# list of 26-entry child tables, each word walked until the first root
# ends, the words split on spaces and joined back.


def replace_words(dictionary, sentence):
    nxt = [[0] * 26]
    ends = [False]
    for root in dictionary:
        node = 0
        for ch in root:
            c = ord(ch) - 97
            if nxt[node][c] == 0:
                nxt[node][c] = len(nxt)
                nxt.append([0] * 26)
                ends.append(False)
            node = nxt[node][c]
        ends[node] = True
    out = []
    for word in sentence.split(" "):
        node = 0
        length = 0
        while length < len(word) and not ends[node]:
            node = nxt[node][ord(word[length]) - 97]
            if node == 0:
                break
            length += 1
        if node != 0 and ends[node]:
            out.append(word[:length])
        else:
            out.append(word)
    return " ".join(out)


seed = 648


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(shortest, longest, letters):
    n = shortest + next_random() % (longest - shortest + 1)
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    inputs = 20
    rounds = 100
    dictionaries = []
    sentences = []
    for _ in range(inputs):
        letters = 3 + next_random() % 6
        roots = [random_word(3, 6, letters) for _ in range(1000)]
        words = [random_word(1, 10, letters) for _ in range(20000)]
        dictionaries.append(roots)
        sentences.append(" ".join(words))
    total = 0
    checksum = 0
    for r in range(rounds):
        i = (r * 7) % inputs
        out = replace_words(dictionaries[i], sentences[i])
        for ch in out:
            total += 1
            checksum = (checksum * 31 + ord(ch)) % 1000000007
    print(f"{inputs} inputs, {rounds} rounds: {total} characters, checksum {checksum}")


main()
