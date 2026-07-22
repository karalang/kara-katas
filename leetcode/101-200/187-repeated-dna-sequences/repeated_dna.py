"""LeetCode 187 — Repeated DNA Sequences (Python mirror / oracle).

Slide a width-10 window, count each 10-mer in a dict, and record a sequence the
first time its count crosses 1 -> 2 (first-repeat order). Mirrors the Kāra version.
"""


def find_repeated(s):
    n = len(s)
    counts = {}
    result = []
    i = 0
    while i + 10 <= n:
        sub = s[i:i + 10]
        c = counts.get(sub, 0)
        if c == 1:
            result.append(sub)
        counts[sub] = c + 1
        i += 1
    return result


def report(s):
    reps = find_repeated(s)
    print(len(reps))
    for r in reps:
        print(r)
    print("---")


def main():
    report("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")
    report("AAAAAAAAAAAAA")
    report("AAAAAAAAAA")
    report("ACGTACGTAC")
    report("GGGGGGGGGGGGGGGGGGGGGGGGG")


main()
