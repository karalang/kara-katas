"""LeetCode #30: Substring with Concatenation of All Words — sliding window.

Algorithmic mirror of sliding_window.kara. Output format matches line-for-line
(the result count, then each ascending start index on its own line).

O(n): run L phases (one per residue r mod L); within a phase, slide a
variable-width window over whole L-byte words, extending on the right and
dropping words off the left whenever a word over-fills its `need` allowance.
Results are sorted before printing so the order matches brute_force.py.
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

    for r in range(wl):
        seen: dict[str, int] = {}
        count = 0
        left = r
        j = r
        while j + wl <= n:
            piece = s[j:j + wl]
            req = need.get(piece, -1)
            if req < 0:
                seen.clear()
                count = 0
                left = j + wl
            else:
                seen[piece] = seen.get(piece, 0) + 1
                count += 1
                while seen.get(piece, 0) > req:
                    lw = s[left:left + wl]
                    seen[lw] = seen.get(lw, 0) - 1
                    left += wl
                    count -= 1
                if count == k:
                    result.append(left)
                    lw = s[left:left + wl]
                    seen[lw] = seen.get(lw, 0) - 1
                    left += wl
                    count -= 1
            j += wl
    result.sort()
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
