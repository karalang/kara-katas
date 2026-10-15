# LeetCode #680: Valid Palindrome II -- two pointers.
# Mirrors the ★ arm (valid_palindrome_ii.kara) and its test harness.


def is_palindrome(s, lo, hi):
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def valid_palindrome(s):
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return is_palindrome(s, i + 1, j) or is_palindrome(s, i, j - 1)
        i += 1
        j -= 1
    return True


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def b(x):
    return "true" if x else "false"


def letter(d):
    return chr(97 + d)


def show(s):
    print(f'"{s}" -> {b(valid_palindrome(s))}')


def nth_string(i, n):
    p = 3 ** (n - 1)
    out = []
    for _ in range(n):
        out.append(letter(i // p % 3))
        p //= 3
    return "".join(out)


def near_palindrome(rng, n, width, extra):
    half = [letter(rng.next() % width) for _ in range(n // 2)]
    cs = list(half)
    if n % 2 == 1:
        cs.append(letter(rng.next() % width))
    cs.extend(reversed(half))
    for _ in range(extra):
        at = rng.next() % (len(cs) + 1)
        cs.insert(at, letter(rng.next() % width))
    return "".join(cs)


def main():
    for s in ["aba", "abca", "abc", "a", "ab", "deeee", "cbbcc", "abcda",
              "tebbem", "abccbxa", "eeccccbebaeeabebccceea",
              "ebcbbececabbacecbbcbe",
              "aguokepatgbnvfqmgmlcupuufxoohdfpgjdmysgvhmvffcnqxjjxqncffvmhvgsymdjgpfdhooxfuupuculmgmqfvnbgtapekouga"]:
        show(s)
    counts = ""
    total = 0
    size = 3
    for n in range(1, 10):
        valid = sum(1 for i in range(size) if valid_palindrome(nth_string(i, n)))
        counts += f" {valid}"
        total += size
        size *= 3
    print(f"strings over abc of length 1 to 9 ({total}), valid by length:{counts}")
    rng = Rng(680)
    long = ""
    for extra in range(3):
        for width in [2, 26]:
            s = near_palindrome(rng, 100000, width, extra)
            long += f" {b(valid_palindrome(s))}"
    print(f"100000 letters, 0, 1, 2 inserted, over 2 and 26 letters:{long}")
    checksum = 0
    valid = 0
    agree = 0
    cases = 3000
    for c in range(cases):
        n = 1 + rng.next() % 40
        width = 1 + rng.next() % 4
        extra = rng.next() % 3
        if c % 2 == 0:
            s = near_palindrome(rng, n, width, extra)
        else:
            s = "".join(letter(rng.next() % width) for _ in range(n))
        ok = valid_palindrome(s)
        if ok:
            valid += 1
            checksum = (checksum * 31 + c + 1) % 1000000007
        if valid_palindrome(s[::-1]) == ok:
            agree += 1
    print(f"{valid} of {cases} random strings valid, checksum {checksum}")
    print(f"{agree} of {cases} answer the same reversed")


main()
