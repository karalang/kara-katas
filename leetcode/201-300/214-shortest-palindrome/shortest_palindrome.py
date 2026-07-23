"""LeetCode 214 — Shortest Palindrome (Python mirror / oracle).

Longest palindromic prefix via the KMP prefix-function of s + '#' + reverse(s);
prepend the reverse of the remaining tail. Mirrors the Kara version.
"""


def shortest_palindrome(s):
    cs = list(s)
    n = len(cs)
    if n == 0:
        return ""

    comb = cs + ['#'] + cs[::-1]
    m = len(comb)

    fail = [0] * m
    length = 0
    idx = 1
    while idx < m:
        if comb[idx] == comb[length]:
            length += 1
            fail[idx] = length
            idx += 1
        elif length > 0:
            length = fail[length - 1]
        else:
            fail[idx] = 0
            idx += 1

    lps = fail[m - 1]
    out = []
    j = n - 1
    while j >= lps:
        out.append(cs[j])
        j -= 1
    out.extend(cs)
    return "".join(out)


def report(s):
    print(shortest_palindrome(s))


def main():
    report("aacecaaa")
    report("abcd")
    report("")
    report("a")
    report("aabba")
    report("aaaa")
    report("ba")
    report("abacd")
    report("abbacd")


main()
