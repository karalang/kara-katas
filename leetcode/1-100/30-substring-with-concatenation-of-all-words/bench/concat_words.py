"""Benchmark workload — substring-with-concatenation, LeetCode #30 (sliding window).

Algorithmic mirror of concat_words.kara: same 16-word vocabulary, same glibc
LCG (high bits for the vocab pick), same NSLOTS / RUNS, same O(n) sliding-window
search, same sink (sum of matched start indices + match counts over all runs).
Prints the identical sink so bench.sh can cross-check against the compiled
mirrors.
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
    return result


def main() -> None:
    nslots = 50000
    runs = 40

    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/"
    vocab = [chars[v * 4:v * 4 + 4] for v in range(16)]

    parts: list[str] = []
    state = 1
    for _ in range(nslots):
        state = (state * 1103515245 + 12345) % 2147483648
        v = (state // 131072) % 16
        parts.append(vocab[v])
    s = "".join(parts)

    sink = 0
    for run in range(runs):
        start = run % 13
        words_r = [vocab[start + d] for d in range(4)]
        res = find_substring(s, words_r)
        sink += len(res)
        for idx in res:
            sink += idx

    print(sink)


if __name__ == "__main__":
    main()
