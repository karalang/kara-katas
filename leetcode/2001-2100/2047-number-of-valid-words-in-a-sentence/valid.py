# LeetCode #2047: Number of Valid Words in a Sentence -- Python mirror of
# the ★ arm (valid.kara): the sentence split at runs of spaces, each token
# checked character by character. Output is byte-identical to the Kāra arms.


def is_valid(token):
    n = len(token)
    hyphens = 0
    for i, c in enumerate(token):
        if c.isdigit():
            return False
        if c == "-":
            hyphens += 1
            if hyphens > 1 or i == 0 or i == n - 1:
                return False
            if not token[i - 1].islower() or not token[i + 1].islower():
                return False
        if c in "!.," and i != n - 1:
            return False
    return True


def count_valid_words(sentence):
    return sum(1 for token in sentence.split() if is_valid(token))


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(length, alphabet):
    s = []
    for _ in range(length):
        r = next_random() % 100
        if r < 60:
            s.append(alphabet[next_random() % 3])
        elif r < 80:
            s.append(" ")
        else:
            s.append(alphabet[next_random() % len(alphabet)])
    s.append("a")
    return "".join(s)


def main():
    global seed
    examples = [
        "cat and  dog",
        "!this  1-s b8d!",
        "alice and  bob are playing stone-game10",
        "he bought 2 pencils, 3 erasers, and 1  pencil-sharpener.",
        "a-b-c a- -a a-b. a-b! ab, a!b ., ,. - !",
        "  x  ",
        "a--b a-. -. q-r-,",
    ]
    for s in examples:
        print(f'"{s}" -> {count_valid_words(s)}')
    seed = 2047
    total = check = 0
    for _ in range(2000):
        length = next_random() % 40
        n = count_valid_words(draw(length, "abc-!.,0123456789"))
        total += n
        check = (check * 31 + n) % 1000000007
    print(f"2000 sentences: {total} valid words, checksum {check}")
    total = check = 0
    for _ in range(3000):
        n = count_valid_words(draw(999, "ab---!!..,,9"))
        total += n
        check = (check * 31 + n) % 1000000007
    print(f"3000 long sentences: {total} valid words, checksum {check}")


main()
