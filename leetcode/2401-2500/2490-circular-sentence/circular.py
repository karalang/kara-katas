# LeetCode #2490: Circular Sentence -- Python mirror of the ★ arm
# (circular.kara): every space with the same letter on both sides, and the
# last letter the first.


def is_circular_sentence(sentence):
    n = len(sentence)
    if sentence[0] != sentence[n - 1]:
        return False
    for i in range(1, n - 1):
        if sentence[i] == " " and sentence[i - 1] != sentence[i + 1]:
            return False
    return True


# ---- test harness -----------------------------------------------------------

seed = 2490


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_sentence(words, longest, letters):
    pool = list(letters)
    parts = []
    last = pool[0]
    for w in range(words):
        length = next_random() % longest + 1
        word = []
        for i in range(length):
            if i == 0 and w > 0 and next_random() % 2 == 0:
                word.append(last)
            else:
                word.append(pool[next_random() % len(pool)])
        last = word[-1]
        parts.append("".join(word))
    return " ".join(parts)


def show(b):
    return "true" if b else "false"


def main():
    cases = [
        "leetcode exercises sound delightful",
        "eetcode",
        "Leetcode is cool",
        "a",
        "ab",
        "aa a",
        "Aa a",
        "ab ba",
        "ab bc ca",
        "ab bc cb",
        "I Ii iI",
    ]
    for s in cases:
        print(f'"{s}" -> {show(is_circular_sentence(s))}')
    for letters in ["aAb", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]:
        circular = 0
        check = 0
        for t in range(3000):
            words = next_random() % 10 + 1
            s = random_sentence(words, 5, letters)
            if is_circular_sentence(s):
                circular += 1
                check = (check * 31 + t + len(s)) % 1000000007
        print(f"3000 random from {len(letters)} letters: {circular} circular, checksum {check}")
    one = "a" * 500
    many = " ".join(["b"] * 250)
    broken = "b " * 249 + "c"
    print(f"one word of 500 -> {show(is_circular_sentence(one))}")
    print(f"250 words of one letter -> {show(is_circular_sentence(many))}")
    print(f"the last one changed -> {show(is_circular_sentence(broken))}")


main()
