#!/usr/bin/env python3
"""Benchmark harness for LeetCode #126 — Word Ladder II.

Mirrors word_ladder_ii.kara algorithm-for-algorithm. Kept as a correctness
oracle for the sink; Python is not a measured lane (see ../README.md).
"""

import sys

MOD = 1000000007
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
    for i in range(len(word)):
        orig = ord(word[i])
        for c in range(26):
            ch = nth_letter(c)
            if (c + 97) != orig:
                cand = replace_char(word, i, ch)
                if cand in word_set:
                    out.append(cand)
    return out


def path_digest(path):
    h = 0
    for idx in range(len(path) - 1, -1, -1):
        for b in path[idx].encode():
            h = (h * 131 + (b - 96)) % MOD
        h = (h * 131 + 27) % MOD
    return h


def dfs(word, begin, preds, path, state):
    if word == begin:
        state[1] = (state[1] + path_digest(path)) % MOD
        state[0] += 1
        return
    plist = preds.get(word)
    if plist is None:
        return
    for p in list(plist):
        path.append(p)
        dfs(p, begin, preds, path, state)
        path.pop()


def find_ladders(begin, end, words):
    word_set = {}
    for w in words:
        word_set[w] = 1
    if end not in word_set:
        return (0, 0, 0)

    preds = {}
    visited = {begin: 1}
    cur = [begin]
    found = False
    depth = 1

    while len(cur) > 0 and not found:
        in_next = {}
        nxt = []
        for word in cur:
            for nb in neighbors(word, word_set):
                if nb not in visited:
                    plist = list(preds.get(nb, []))
                    plist.append(word)
                    preds[nb] = plist
                    if nb not in in_next:
                        if nb == end:
                            found = True
                        in_next[nb] = 1
                        nxt.append(nb)
        for w in nxt:
            visited[w] = 1
        cur = nxt
        depth += 1

    if not found:
        return (0, 0, 0)

    path = [end]
    state = [0, 0]
    dfs(end, begin, preds, path, state)
    return (state[0], depth, state[1])


def main():
    sys.setrecursionlimit(10000)
    alpha = 5
    wlen = 5
    iters = 24
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
        count, length, digest = find_ladders(words[b], words[e], words)
        sink = (sink * 1000003 + count * 7 + length * 13 + digest) % MOD
    print(sink)


main()
