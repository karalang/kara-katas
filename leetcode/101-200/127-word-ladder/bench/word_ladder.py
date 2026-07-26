#!/usr/bin/env python3
"""Benchmark harness for LeetCode #127 — Word Ladder.

Mirrors word_ladder.kara algorithm-for-algorithm. Kept as a correctness oracle
for the sink; Python is not a measured lane (see ../README.md).
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def nth_letter(n):
    return ALPHABET[n % 26]


def replace_char(word, pos, new_ch):
    out = []
    for i, ch in enumerate(word):
        if i == pos:
            out.append(new_ch)
        else:
            out.append(ch)
    return "".join(out)


def neighbors(word, word_set):
    out = []
    n = len(word)
    for i in range(n):
        orig = ord(word[i])
        for c in range(26):
            if (c + 97) != orig:
                cand = replace_char(word, i, nth_letter(c))
                if cand in word_set:
                    out.append(cand)
    return out


def ladder_length(begin, end, words):
    word_set = {}
    for w in words:
        word_set[w] = 1
    if end not in word_set:
        return 0

    visited = {begin: 1}
    cur = [begin]
    steps = 1

    while len(cur) > 0:
        nxt = []
        for word in cur:
            if word == end:
                return steps
            for nb in neighbors(word, word_set):
                if nb not in visited:
                    visited[nb] = 1
                    nxt.append(nb)
        cur = nxt
        steps += 1
    return 0


def main():
    alpha = 5
    wlen = 5
    iters = 17
    total = 3125

    words = []
    for idx in range(total):
        w = []
        rem = idx
        div = 625
        for _ in range(wlen):
            digit = rem // div
            w.append(nth_letter(digit))
            rem -= digit * div
            div //= alpha
        words.append("".join(w))

    sink = 0
    for it in range(iters):
        b = (it * 257) % total
        e = (it * 613 + 1234) % total
        r = ladder_length(words[b], words[e], words)
        sink = (sink * 31 + r) % 1000000007
    print(sink)


main()
