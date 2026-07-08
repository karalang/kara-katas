"""Benchmark workload — Text Justification (LeetCode #68).

Python mirror of bench/text_justification.kara. The ★'s greedy-pack + even-spread
logic streaming emitted bytes (word chars + gap spaces) into the same rolling
polynomial hash — no line-string building. CPython is multi-second at the
compiled mirrors' K=300_000, so this runs K=30_000 (1/10th) — timed separately
and NOT cross-checked against the compiled sink. See ../README.md § Benchmarks.
"""

from __future__ import annotations

WORDS = ["the", "quick", "brown", "fox", "jumps", "over", "a", "lazy", "dog", "while",
         "gentle", "breeze", "carries", "autumn", "leaves", "across", "quiet", "meadow",
         "near", "old", "stone", "bridge", "where", "children", "often", "gather", "to",
         "watch", "river", "flow", "beneath", "ancient", "willow", "trees", "and",
         "listen", "as", "the", "wind", "hums"]
NW = len(WORDS)
MOD = 1_000_000_007


def justify_hash(max_width: int, h: int) -> int:
    i = 0
    while i < NW:
        j = i
        line_chars = 0
        count = 0
        while j < NW:
            wl = len(WORDS[j])
            if line_chars + wl + count <= max_width:
                line_chars += wl
                count += 1
                j += 1
            else:
                break
        gaps = count - 1
        total = max_width - line_chars
        is_last = j == NW

        if is_last or count == 1:
            used = 0
            for g in range(count):
                for c in WORDS[i + g]:
                    h = (h * 131 + ord(c)) % MOD
                    used += 1
                if g < count - 1:
                    h = (h * 131 + 32) % MOD
                    used += 1
            while used < max_width:
                h = (h * 131 + 32) % MOD
                used += 1
        else:
            base = total // gaps
            extra = total % gaps
            for g in range(count):
                for c in WORDS[i + g]:
                    h = (h * 131 + ord(c)) % MOD
                if g < gaps:
                    sp = base + (1 if g < extra else 0)
                    for _ in range(sp):
                        h = (h * 131 + 32) % MOD
        i = j
    return h


def main() -> None:
    total = 30_000
    span = 40

    acc = 0
    for k in range(total):
        width = 10 + (k % span)
        acc = justify_hash(width, acc)
    print(acc)


if __name__ == "__main__":
    main()
