"""LeetCode 161 — One Edit Distance (Python mirror / oracle). Premium.

True iff s and t are exactly one edit (insert/delete/replace of one char) apart.
Single linear scan with the shorter string on the left. Mirrors the Kāra version.
"""


def is_one_edit(s, t):
    a, b = s, t
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    if n - m > 1:
        return False
    for i in range(m):
        if a[i] != b[i]:
            if m == n:
                return a[i + 1:] == b[i + 1:]   # replace
            return a[i:] == b[i + 1:]           # insert
    return n - m == 1


def report(s, t):
    print("true" if is_one_edit(s, t) else "false")


def main():
    report("ab", "acb")
    report("cab", "ad")
    report("1203", "1213")
    report("", "")
    report("", "a")
    report("a", "")
    report("abc", "abc")
    report("abc", "abcd")
    report("abc", "abcde")
    report("teacher", "teachers")


main()
