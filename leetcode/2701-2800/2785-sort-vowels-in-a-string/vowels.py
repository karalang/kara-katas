# LeetCode #2785: Sort Vowels in a String -- the ★ arm in Python
# (vowels.kara): the vowels gathered, sorted, and written back into the
# vowels' places in order.


def is_vowel(c):
    return c in "aeiouAEIOU"


def sort_vowels(s):
    vowels = sorted(c for c in s if is_vowel(c))
    out = []
    nxt = 0
    for c in s:
        if is_vowel(c):
            out.append(vowels[nxt])
            nxt += 1
        else:
            out.append(c)
    return "".join(out)


seed = 2785


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(letters[next_random() % len(letters)] for _ in range(n))


def fold(s, check):
    for b in s.encode():
        check = (check * 31 + b) % 1000000007
    return check


def main():
    print(sort_vowels("lEetcOde"))
    print(sort_vowels("lYmpH"))
    print(sort_vowels("uoieaUOIEA"))
    print(sort_vowels("bcdfgXYZ"))
    print(sort_vowels("a"))
    check = 0
    letters = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        t = sort_vowels(random_text(n, "aeiouAEIOUbcxyZB"))
        letters += len(t)
        check = fold(t, check)
    print(f"3000 small strings: {letters} letters, checksum {check}")
    check = 0
    every = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for _ in range(3):
        t = sort_vowels(random_text(100000, every))
        check = fold(t, check)
    print(f"3 strings of 10^5: checksum {check}")


main()
