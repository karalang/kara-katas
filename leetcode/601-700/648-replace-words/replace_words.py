# LeetCode #648: Replace Words -- a trie of the roots.
# Mirrors the ★ arm (replace_words.kara) and its test harness.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(dictionary, sentence):
    print(f'[{",".join(dictionary)}] "{sentence}" -> "{replace_words(dictionary, sentence)}"')


def random_word(shortest, longest, letters):
    n = shortest + next_random() % (longest - shortest + 1)
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def random_words(count, shortest, longest, letters):
    return [random_word(shortest, longest, letters) for _ in range(count)]


def digest(s, state):
    for ch in s:
        state[0] += 1
        state[1] = (state[1] * 31 + ord(ch)) % 1000000007
    state[1] = (state[1] * 31 + 1) % 1000000007


def main():
    global seed
    show(["cat", "bat", "rat"], "the cattle was rattled by the battery")
    show(["a", "b", "c"], "aadsfasf absbs bbab cadsfafs")
    show(["cat"], "cat cats ca")
    show(["catalog"], "cat catalogue")
    show(["aaa", "aa", "a"], "aaaa baaa")
    show(["xyz", "q"], "abc def")
    show(["be", "be"], "bed bee be b")
    show(["e"], "e")
    seed = 648
    state = [0, 0]
    for _ in range(300):
        roots = random_words(1 + next_random() % 10, 1, 4, 3)
        words = random_words(1 + next_random() % 10, 1, 8, 3)
        digest(replace_words(roots, " ".join(words)), state)
    print(f"300 random cases: {state[0]} characters, checksum {state[1]}")
    for letters in [4, 26]:
        roots = random_words(1000, 3, 6, letters)
        words = random_words(5000, 1, 10, letters)
        st = [0, 0]
        digest(replace_words(roots, " ".join(words)), st)
        print(f"1000 roots, 5000 words of {letters} letters: {st[0]} characters, checksum {st[1]}")


main()
