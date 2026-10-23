# LeetCode #884: Uncommon Words from Two Sentences -- Python mirror of the
# one-map solution in uncommon_from_sentences.kara, with the same test
# harness.
#
# A word that appears exactly once in one sentence and not at all in the
# other appears exactly once in the two sentences together, and the
# converse holds too. So the words of both sentences are counted in one
# map, and the answer is the words counted once. O(total length).


def uncommon_from_sentences(s1, s2):
    counts = {}
    for word in s1.split(" "):
        counts[word] = counts.get(word, 0) + 1
    for word in s2.split(" "):
        counts[word] = counts.get(word, 0) + 1
    return [word for word, n in counts.items() if n == 1]


# ---- test harness ----------------------------------------------------------


def sorted_answer(s1, s2):
    return sorted(uncommon_from_sentences(s1, s2))


def text(words):
    return "[" + ", ".join(words) + "]"


def show(s1, s2):
    shown1 = f"{len(s1)} characters" if len(s1) > 40 else f'"{s1}"'
    shown2 = f"{len(s2)} characters" if len(s2) > 40 else f'"{s2}"'
    print(f"s1 = {shown1}, s2 = {shown2} -> {text(sorted_answer(s1, s2))}")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a sentence of at most `limit` characters, at least one word, of words of
# 1 to `longest` letters from the first `letters` of the alphabet, ending
# after each word with chance 1 in `stop`
def sentence(limit, longest, letters, stop):
    out = ""
    while True:
        size = next_random() % longest + 1
        word = ""
        for _ in range(size):
            word += chr(97 + next_random() % letters)
        if len(out) == 0:
            out = word
        elif len(out) + 1 + len(word) <= limit:
            out = out + " " + word
        else:
            return out
        if next_random() % stop == 0:
            return out


def fold(check, words):
    c = check
    for w in words:
        for b in w.encode():
            c = (c * 131 + b) % 1000000007
        c = (c * 131 + 44) % 1000000007
    return (c * 131 + 59) % 1000000007


def main():
    global seed
    show("this apple is sweet", "this apple is sour")
    show("apple apple", "banana")
    show("a", "b")
    show("a", "a")
    show("a a a", "b")
    show("x y z", "z y x")
    show("go to the store and buy the milk", "the milk is at the store")
    long1 = "w"
    long2 = "q"
    for i in range(99):
        long1 = long1 + " " + ("u" if i % 2 == 0 else "w")
        long2 = long2 + " " + ("z" if i == 98 else "q")
    show(long1, long2)
    # small cases
    seed = 884
    total = 0
    check = 0
    for _ in range(3000):
        s1 = sentence(20, 2, 3, 5)
        s2 = sentence(20, 2, 3, 5)
        words = sorted_answer(s1, s2)
        total += len(words)
        check = fold(check, words)
    print(f"3000 pairs of up to 20 characters: {total} uncommon words, checksum {check}")
    # LeetCode's sizes: up to 200 characters
    total = 0
    check = 0
    for _ in range(1000):
        s1 = sentence(200, 4, 5, 80)
        s2 = sentence(200, 4, 5, 80)
        words = sorted_answer(s1, s2)
        total += len(words)
        check = fold(check, words)
    print(f"1000 pairs of up to 200 characters: {total} uncommon words, checksum {check}")


main()
