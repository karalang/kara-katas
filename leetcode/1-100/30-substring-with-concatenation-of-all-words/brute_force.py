"""LeetCode #30: Substring with Concatenation of All Words — brute force.

Algorithmic mirror of brute_force.kara. Output format matches line-for-line
(the result count, then each start index on its own line) so the two can be
diffed directly.

Brute force: build a `need` multiset once, then try every start `i` and tally
the K consecutive L-byte pieces of the window into a fresh `seen` map, bailing
on the first piece that is unknown or over its allowance.
"""

from __future__ import annotations


def find_substring(s: str, words: list[str]) -> list[int]:
    result: list[int] = []
    k = len(words)
    if k == 0:
        return result
    wl = len(words[0])
    total = wl * k
    n = len(s)
    if wl == 0 or total > n:
        return result

    need: dict[str, int] = {}
    for w in words:
        need[w] = need.get(w, 0) + 1

    i = 0
    while i + total <= n:
        seen: dict[str, int] = {}
        ok = True
        j = 0
        while j < k:
            start = i + j * wl
            piece = s[start:start + wl]
            req = need.get(piece, -1)
            if req < 0:
                ok = False
                j = k
            else:
                cur = seen.get(piece, 0)
                if cur + 1 > req:
                    ok = False
                    j = k
                else:
                    seen[piece] = cur + 1
                    j += 1
        if ok:
            result.append(i)
        i += 1
    return result


def report(s: str, words: list[str]) -> None:
    r = find_substring(s, words)
    print(len(r))
    for idx in r:
        print(idx)


def main() -> None:
    report("barfoothefoobarman", ["foo", "bar"])              # 2: 0 9
    report("wordgoodgoodgoodbestword", ["word", "good", "best", "word"])  # 0
    report("barfoofoobarthefoobarman", ["bar", "foo", "the"])  # 3: 6 9 12
    report("aaaaaa", ["aa", "aa"])                            # 3: 0 1 2
    report("abababab", ["a", "b", "a"])                       # 3: 0 2 4
    report("a", ["a"])                                        # 1: 0
    report("abbaab", ["ab", "ba"])                            # 2: 0 2


if __name__ == "__main__":
    main()
