"""LeetCode 151 — Reverse Words in a String (Python mirror / oracle).

Collect each maximal non-space run as a word (one byte scan), then emit the
words back-to-front joined by a single space — no leading/trailing/repeated
spaces regardless of the input's spacing. Mirrors the Kāra version's
`s[start:i]` word slices.
"""


def reverse_words(s):
    words = []
    n = len(s)
    i = 0
    while i < n:
        while i < n and s[i] == " ":
            i += 1
        if i >= n:
            break
        start = i
        while i < n and s[i] != " ":
            i += 1
        words.append(s[start:i])
    out = []
    for k in range(len(words) - 1, -1, -1):
        out.append(words[k])
    return " ".join(out)


def run(s):
    print(reverse_words(s))


def main():
    run("the sky is blue")
    run("  hello world  ")
    run("a good   example")
    run("single")
    run("   ")
    run("  leading and trailing  ")


main()
