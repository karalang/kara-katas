# Mirror of string_matching.kara: every word some other word contains.


def string_matching(words):
    return [w for w in words if any(o != w and w in o for o in words)]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, length, letters):
    words = []
    while len(words) < n:
        size = 1 + next_random() % length
        word = "".join(chr(ord("a") + next_random() % letters) for _ in range(size))
        if word not in words:
            words.append(word)
    return words


def shown(words):
    return "[" + ",".join(sorted(string_matching(words))) + "]"


def main():
    global seed
    print(" ".join(shown(w) for w in [["mass", "as", "hero", "superhero"], ["leetcode", "et", "code"], ["blue", "green", "bu"],
                                      ["a"], ["a", "aa", "aaa", "aaaa"], ["ab", "ba", "aba", "bab"]]))
    seed = 1408
    two = string_matching(drawn(100, 30, 2))
    many = string_matching(drawn(100, 30, 26))
    print(f"100 words: {len(two)} {len(many)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 20
        found = sorted(string_matching(drawn(n, 6, 3)))
        total += len(found)
        for w in found:
            for c in w:
                check = (check * 131 + ord(c)) % 1000000007
            check = (check * 131 + 1) % 1000000007
    print(f"2000 random sets: {total} found, checksum {check}")


main()
