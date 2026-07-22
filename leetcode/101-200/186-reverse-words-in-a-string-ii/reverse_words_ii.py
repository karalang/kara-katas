"""LeetCode 186 — Reverse Words in a String II (Python mirror / oracle). Premium.

In-place on a char array: reverse the whole array, then reverse each word back.
Mirrors the Kāra version (list of chars, index swaps).
"""


def reverse_range(a, lo, hi):
    i, j = lo, hi
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def reverse_words(s):
    a = list(s)
    n = len(a)
    if n > 0:
        reverse_range(a, 0, n - 1)
    start = 0
    i = 0
    while i <= n:
        if i == n or a[i] == " ":
            if i > start:
                reverse_range(a, start, i - 1)
            start = i + 1
        i += 1
    return "".join(a)


def report(s):
    print(reverse_words(s))


def main():
    report("the sky is blue")
    report("hello world")
    report("a")
    report("a b c")
    report("perfect makes practice")


main()
