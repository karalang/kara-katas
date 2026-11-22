# LeetCode #2828: Check if a String Is an Acronym of Words -- the
# bench's Python mirror of the ★ arm: the lengths first, then every
# word's first byte against s's byte at the same place.


def is_acronym(words, s):
    b = s.encode()
    return len(words) == len(b) and all(w.encode()[0] == c for w, c in zip(words, b))


seed = 2828


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word():
    n = next_random() % 10 + 1
    return "".join(chr(97 + next_random() % 3) for _ in range(n))


def main():
    count, rounds = 20000, 100
    cases = []
    for _ in range(count):
        words = [word() for _ in range(100)]
        s = [w.encode()[0] for w in words]
        if next_random() % 4 == 0:
            at = next_random() % 100
            s[at] = 97 + next_random() % 3
        cases.append((words, bytes(s).decode()))
    yes = 0
    check = 0
    for r in range(rounds):
        for words, s in cases:
            a = is_acronym(words, s)
            yes += a
            check = (check * 31 + (1 if a else 0) + r) % 1000000007
    print(f"{count} cases of 100 words, {rounds} rounds: {yes} true, checksum {check}")


main()
