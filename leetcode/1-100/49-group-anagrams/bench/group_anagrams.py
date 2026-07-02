"""Benchmark workload — sorted-key Group Anagrams (LeetCode #49).

Algorithmic mirror of bench/group_anagrams.kara. See ../README.md § Benchmarks
for the input shape (N=20_000 words, L=8, G=1_000 classes) and K choice.
The deterministic generator produces 26 distinct anagram classes (each class's
letters are L consecutive alphabet letters mod 26), so every call groups the
20_000 words into 26 groups; sink = K * 26 = 40 * 26 = 1040.
"""

from __future__ import annotations

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def count_groups(words: list[str]) -> int:
    index_of: dict[str, int] = {}
    groups = 0
    for w in words:
        key = "".join(sorted(w))
        if key not in index_of:
            index_of[key] = groups
            groups += 1
    return groups


def make_words(n: int, g: int, ln: int) -> list[str]:
    words: list[str] = []
    for i in range(n):
        grp = i % g
        rot = (i // g) % ln
        seed = "".join(ALPHABET[(grp + k) % 26] for k in range(ln))
        words.append(seed[rot:ln] + seed[0:rot])
    return words


def main() -> None:
    words = make_words(20000, 1000, 8)
    total = 0
    for _ in range(40):
        total += count_groups(words)
    print(total)


if __name__ == "__main__":
    main()
