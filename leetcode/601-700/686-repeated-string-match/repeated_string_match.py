# LeetCode #686: Repeated String Match -- repeat until long enough.
# Mirrors the ★ arm (repeated_string_match.kara) and its test harness.


def repeated_string_match(a, b):
    n = len(a)
    m = len(b)
    q = (m + n - 1) // n
    s = a * q
    if b in s:
        return q
    s += a
    q += 1
    if b in s:
        return q
    return -1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(a, b):
    print(f"a = {a}, b = {b} -> {repeated_string_match(a, b)}")


# The string of `length` letters from `letters` that `code` numbers.
def word(code, length, letters):
    s = []
    c = code
    for _ in range(length):
        s.append(chr(97 + c % letters))
        c //= letters
    return "".join(s)


def random_word(rng, length, letters):
    return "".join(chr(97 + rng.next() % letters) for _ in range(length))


# `length` letters of the repetition of `a`, from position `start`.
def slice_of_repeats(a, start, length):
    n = len(a)
    return "".join(a[(start + i) % n] for i in range(length))


def main():
    show("abcd", "cdabcdab")
    show("a", "aa")
    show("abc", "wxyz")
    show("abc", "abc")
    show("abc", "cabcabca")
    show("aa", "a")
    show("ab", "ba")
    show("abab", "aba")
    show("abc", "cba")
    show("a", "aaaaaaaaaa")
    show("abcabcabcabc", "abac")
    show("baa", "abaab")

    # Every `a` of 1 to 4 letters and `b` of 1 to 7 over two letters.
    counts = [0] * 8
    total = 0
    for la in range(1, 5):
        for ca in range(1 << la):
            a = word(ca, la, 2)
            for lb in range(1, 8):
                for cb in range(1 << lb):
                    r = repeated_string_match(a, word(cb, lb, 2))
                    counts[0 if r == -1 else r] += 1
                    total = (total * 31 + r + 2) % 1000000007
    print(f"two letters, a up to 4 and b up to 7: by answer -1 and 1 to 7 {counts}, checksum {total}")

    # Random pairs: half of them `b` cut from the repetition of `a`, one
    # in four of those with a letter changed.
    rng = Rng(686)
    none = 0
    checksum = 0
    for c in range(300):
        n = 1 + rng.next() % 40
        letters = 1 + rng.next() % 3
        a = random_word(rng, n, letters)
        m = 1 + rng.next() % (4 * n + 4)
        if c % 2 == 0:
            start = rng.next() % n
            s = slice_of_repeats(a, start, m)
            if rng.next() % 4 == 0:
                at = rng.next() % m
                t = list(s)
                t[at] = chr(97 + rng.next() % 3)
                b = "".join(t)
            else:
                b = s
        else:
            b = random_word(rng, m, letters)
        r = repeated_string_match(a, b)
        if r == -1:
            none += 1
        checksum = (checksum * 31 + r + 2) % 1000000007
    print(f"300 random pairs: {none} with no answer, checksum {checksum}")

    # Long strings: `a` of 10,000 letters and `b` of 10,000 cut from
    # its repetition, and the same `b` with its last letter changed.
    for _ in range(3):
        a = random_word(rng, 10000, 26)
        start = rng.next() % 10000
        b = slice_of_repeats(a, start, 10000)
        changed = b[:9999] + ("b" if b[9999] == "a" else "a")
        print(f"long: {repeated_string_match(a, b)}, changed: {repeated_string_match(a, changed)}")


main()
