# LeetCode 804 -- Unique Morse Code Words: mirrors the harness of
# unique_morse.kara with the ★ arm's set of strings.
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


def show(words):
    out = "[" + ", ".join(f'"{w}"' for w in words) + "]"
    print(f"{out} -> {unique_morse_representations(words)}")


def main():
    show("gin zen gig msg".split(" "))
    show("a".split(" "))
    show("a et".split(" "))
    show("n te tn".split(" "))
    show("s eee ie ei i e".split(" "))
    show("abcdefghijkl mnopqrstuvwx yz".split(" "))
    show("zzzzzzzzzzzz qqqqqqqqqqqq zzzzzzzzzzzz".split(" "))
    total = 0
    check = 0
    for i in range(300):
        count = 1 + next_random() % 30
        words = []
        for _ in range(count):
            length = 1 + next_random() % 4
            words.append("".join(["e", "i", "t", "a", "m", "n"][next_random() % 6] for _ in range(length)))
        k = unique_morse_representations(words)
        total += k
        check = (check * 131 + k + i) % 1000000007
    print(f"300 random lists: {total} codes in all, checksum {check}")


main()
