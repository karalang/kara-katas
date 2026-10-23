# LeetCode #890 bench: Python mirror of find_and_replace_pattern.kara (the
# table arm, two tables of 26 letters) on the same 6000 words.


def matches(word, pattern):
    to = [-1] * 26
    frm = [-1] * 26
    for i in range(len(pattern)):
        a = pattern[i] - 97
        b = word[i] - 97
        if to[a] < 0 and frm[b] < 0:
            to[a] = b
            frm[b] = a
        elif to[a] != b or frm[b] != a:
            return False
    return True


def find_and_replace_pattern(words, pattern):
    return [word for word in words if matches(word, pattern)]


def main():
    seed = 890

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    words = []
    for _ in range(6000):
        words.append(bytes(97 + next_random() % 3 for _ in range(10)))
    found = 0
    check = 0
    for k in range(len(words)):
        kept = find_and_replace_pattern(words, words[k])
        found += len(kept)
        check = (check * 131 + len(kept)) % 1000000007
    print(f"6000 patterns over 6000 words of 10 letters: {found} matches, checksum {check}")


main()
