# LeetCode #2828: Check if a String Is an Acronym of Words -- the Python
# mirror of the ★ arm: the lengths first, then every word's first byte
# against s's byte at the same place.


def is_acronym(words, s):
    b = s.encode()
    return len(words) == len(b) and all(w.encode()[0] == c for w, c in zip(words, b))


# ---- the harness: the same in every arm --------------------------------

seed = 2828


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word():
    n = next_random() % 10 + 1
    return "".join(chr(97 + next_random() % 3) for _ in range(n))


def show(b):
    return "true" if b else "false"


def main():
    print(show(is_acronym(["alice", "bob", "charlie"], "abc")))
    print(show(is_acronym(["an", "apple"], "a")))
    print(show(is_acronym(["never", "gonna", "give", "up", "on", "you"], "ngguoy")))
    print(show(is_acronym(["z"], "z")))
    print(show(is_acronym(["ab", "ba"], "abba")))
    hundred = [chr(97 + i % 26) + "x" for i in range(100)]
    initials = "".join(chr(97 + i % 26) for i in range(100))
    print(show(is_acronym(hundred, initials)))
    yes = 0
    check = 0
    for _ in range(5000):
        count = next_random() % 100 + 1
        words = [word() for _ in range(count)]
        s = [w.encode()[0] for w in words]
        at = next_random() % len(s)
        op = next_random() % 4
        if op == 0:
            s[at] = 97 + next_random() % 3
        elif op == 1 and len(s) > 1:
            s.pop(at)
        elif op == 2:
            s.insert(at, ord("a"))
        a = is_acronym(words, bytes(s).decode())
        yes += a
        check = (check * 31 + (1 if a else 0) + count) % 1000000007
    print(f"5000 cases: {yes} true, checksum {check}")


main()
