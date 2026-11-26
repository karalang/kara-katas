# LeetCode #1451 Rearrange Words in a Sentence: a mirror of arrange_words.kara.


def arrange_words(text):
    # the words lowered, sorted by length with ties kept in order by the
    # stable sort, joined, and the first letter raised
    words = [w.lower() for w in text.split(" ")]
    words.sort(key=len)
    joined = " ".join(words)
    return joined[:1].upper() + joined[1:]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sentence(n, longest, k):
    words = []
    for i in range(n):
        length = 1 + next_random() % longest
        w = "".join(chr(ord("a") + next_random() % k) for _ in range(length))
        words.append(w.capitalize() if i == 0 else w)
    return " ".join(words)


def fold(s, check):
    for b in s.encode():
        check = (check * 131 + b) % 1000000007
    return check


def main():
    global seed
    for text in ["Leetcode is cool", "Keep calm and code on", "To be or not to be", "A", "Word", "Ab cd"]:
        print(arrange_words(text))
    seed = 1451
    short = "A" + " a" * 49999
    check = fold(arrange_words(short), 0)
    check = fold(arrange_words(sentence(15000, 10, 26)), check)
    print(f"10^5 letters: checksum {check}")
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        longest = 1 + next_random() % 12
        k = 1 + next_random() % 26
        check = fold(arrange_words(sentence(n, longest, k)), check)
    print(f"2000 random texts: checksum {check}")


main()
