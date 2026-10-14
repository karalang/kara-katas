# LeetCode #557: Reverse Words in a String III -- Python mirror of the ★
# arm (split, reverse, join); see reverse_words_in_a_string_iii.kara.


def reverse_words(s):
    return " ".join(w[::-1] for w in s.split(" "))


# ---- test harness ---------------------------------------------------------

seed = 557


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}" -> "{reverse_words(s)}"')


def random_text(words, longest):
    out = []
    for k in range(words):
        if k > 0:
            out.append(" ")
        length = 1 + next_random() % longest
        for _ in range(length):
            out.append(chr(ord("!") + next_random() % 94))
    return "".join(out)


def checksum(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    show("Let's take LeetCode contest")
    show("Mr Ding")
    show("a")
    show("ab cd")
    show("racecar level noon")
    show("12345 !?.,; (x)")
    chars = 0
    h = 0
    for _ in range(300):
        words = 1 + next_random() % 20
        text = random_text(words, 12)
        chars += len(text)
        h = (h * 31 + checksum(reverse_words(text))) % 1000000007
    print(f"300 random texts: {chars} characters, checksum {h}")
    one = "".join(chr(ord("a") + k % 26) for k in range(50000))
    singles = " ".join(chr(ord("a") + k % 26) for k in range(25000))
    for text in (one, singles):
        got = reverse_words(text)
        print(f"{len(text)} characters -> {len(got)}, starting {got[:10]}, checksum {checksum(got)}")


main()
