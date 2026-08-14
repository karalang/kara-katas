"""LeetCode 267 — Palindrome Permutation II (Python mirror / oracle).

Mirrors palindrome_permutation_ii.kara algorithm-for-algorithm: halve the
counts, backtrack over DISTINCT characters to build the first half, and mirror
each arrangement around the optional lone middle.
"""


def build(counts, half, half_len, middle, out):
    if len(half) == half_len:
        s = "".join(chr(c) for c in half)
        if middle >= 0:
            s += chr(middle)
        s += "".join(chr(c) for c in reversed(half))
        out.append(s)
        return
    for c in range(128):
        if counts[c] > 0:
            counts[c] -= 1
            half.append(c)
            build(counts, half, half_len, middle, out)
            half.pop()
            counts[c] += 1


def generate(s):
    counts = [0] * 128
    for b in s.encode():
        counts[b] += 1

    odd, middle, half_len = 0, -1, 0
    for c in range(128):
        if counts[c] % 2 == 1:
            odd += 1
            middle = c
        counts[c] //= 2
        half_len += counts[c]

    out = []
    if odd > 1:
        return out
    build(counts, [], half_len, middle, out)
    return out


def report(s):
    res = generate(s)
    print(f'"{s}" ({len(res)}) [{",".join(res)}]')


def main():
    for s in ("aabb", "abc", "aabbc", "", "a", "aa", "aaa", "aabbcc",
              "aaaabb", "carerac"):
        report(s)


main()
