# LeetCode #1455 Check If a Word Occurs As a Prefix of Any Word in a
# Sentence: a mirror of is_prefix_of_word.kara.


def is_prefix_of_word(sentence, search_word):
    # the first word that starts with the search word, counted from 1
    for i, w in enumerate(sentence.split(" ")):
        if w.startswith(search_word):
            return i + 1
    return -1


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(longest, k):
    n = 1 + next_random() % longest
    return "".join(chr(97 + next_random() % k) for _ in range(n))


def sentence(most, longest, k):
    s = word(longest, k)
    while True:
        w = word(longest, k)
        if len(s) + 1 + len(w) > most:
            break
        s += " " + w
    return s


def main():
    global seed
    cases = [("i love eating burger", "burg"), ("this problem is an easy problem", "pro"), ("i am tired", "you"), ("hello", "hello"), ("a bb ccc", "cccc"), ("abc xbc", "bc")]
    for s, w in cases:
        print(is_prefix_of_word(s, w))
    seed = 1455
    tail = "a"
    while len(tail) < 97:
        tail += " b"
    tail += " c"
    long = sentence(100, 10, 3)
    last = long.split(" ")[-1]
    probe = last[:min(len(last), 3)]
    print(f"100 letters: {is_prefix_of_word(tail, 'c')} and {is_prefix_of_word(long, probe)}")
    found = 0
    check = 0
    for _ in range(2000):
        most = 1 + next_random() % 100
        longest = 1 + next_random() % 6
        k = 1 + next_random() % 3
        s = sentence(most, longest, k)
        w = word(3, k)
        got = is_prefix_of_word(s, w)
        if got > 0:
            found += 1
        check = (check * 131 + got + 1) % 1000000007
    print(f"2000 random cases: {found} found, checksum {check}")


main()
