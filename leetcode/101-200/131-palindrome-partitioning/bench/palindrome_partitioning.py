"""Benchmark harness for LeetCode #131 — Palindrome Partitioning.

Mirrors palindrome_partitioning.kara algorithm-for-algorithm, including the
kata's O(n) `substring` (walk and filter) rather than a native slice. Committed
as the correctness oracle; not a measured lane.
"""

ITERS = 150


def modulus():
    return 1000000007


def is_pal(b, lo, hi):
    l = lo
    h = hi
    while l < h:
        if b[l] != b[h]:
            return False
        l += 1
        h -= 1
    return True


def substring(s, lo, hi):
    out = []
    for i, ch in enumerate(s):
        if lo <= i <= hi:
            out.append(ch)
    return "".join(out)


def part_hash(path):
    m = modulus()
    h = 0
    for piece in path:
        for b in piece.encode():
            h = (h * 131 + (b - 96)) % m
        h = (h * 131 + 27) % m
    return h


def backtrack(s, b, start, n, path, state):
    if start == n:
        m = modulus()
        state[1] = (state[1] + part_hash(path)) % m
        state[0] += 1
        return
    for end in range(start, n):
        if is_pal(b, start, end):
            path.append(substring(s, start, end))
            backtrack(s, b, end + 1, n, path, state)
            path.pop()


def main():
    cases = [
        "aaaaaaaaaaaaaaaa",
        "abababababababab",
        "abcdefghijklmnop",
        "aabaacaabaacaaba",
    ]
    np_ = len(cases)

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % np_
        s = cases[idx]
        b = s.encode()
        n = len(b)
        path = []
        state = [0, 0]  # count, digest
        backtrack(s, b, 0, n, path, state)
        sink = (sink + state[0] * 7 + state[1]) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
