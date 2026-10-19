# LeetCode 804 -- Unique Morse Code Words: the bench, mirroring
# unique_morse.kara with the same set of strings.
seed = 804
CODES = [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---", "-.-", ".-..", "--",
         "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."]


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def morse(word):
    return "".join(CODES[ord(ch) - 97] for ch in word)


def unique_morse_representations(words):
    return len({morse(word) for word in words})


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    short = "etianm"
    lists = []
    for _ in range(64):
        words = []
        for _ in range(100):
            length = 1 + next_random() % 12
            few = next_random() % 2 == 0
            word = []
            for _ in range(length):
                word.append(short[next_random() % 6] if few else letters[next_random() % 26])
            words.append("".join(word))
        lists.append(words)
    rounds = 100000
    total = 0
    check = 0
    for r in range(rounds):
        k = unique_morse_representations(lists[r % 64])
        total += k
        check = (check * 131 + k) % 1000000007
    print(f"{rounds} rounds of 100 words: {total} codes in all, checksum {check}")


main()
