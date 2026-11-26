# LeetCode #1455 bench mirror: the first word that starts with the search
# word, counted from 1.


def is_prefix_of_word(sentence, search_word):
    for i, w in enumerate(sentence.split(" ")):
        if w.startswith(search_word):
            return i + 1
    return -1


seed = 1455


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a word of 1 to `longest` letters drawn from the first 4 of the alphabet
def word(longest):
    n = 1 + next_random() % longest
    return "".join(chr(97 + next_random() % 4) for _ in range(n))


def main():
    # 2000 sentences of 100 letters of words of 1 to 8 letters and 2000
    # search words of 1 to 4 letters, drawn once, then every search word
    # looked for in every sentence, the answers folded to a checksum
    sentences = []
    for _ in range(2000):
        s = word(8)
        while True:
            w = word(8)
            if len(s) + 1 + len(w) > 100:
                break
            s += " " + w
        sentences.append(s)
    searches = [word(4) for _ in range(2000)]
    check = 0
    for s in sentences:
        for w in searches:
            check = (check * 131 + is_prefix_of_word(s, w) + 1) % 1000000007
    print(f"4 x 10^6 searches: checksum {check}")


main()
