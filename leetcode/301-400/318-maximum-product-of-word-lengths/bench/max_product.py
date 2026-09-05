"""Benchmark mirror of LeetCode #318 — build-once + punch.

Same algorithm as bench/max_product.kara: a flat WORDS x LMAX letter grid,
26-bit letter masks rebuilt every pass, and a full pair scan that records each
word's best disjoint partner. One word is rewritten per pass."""

WORDS = 6000
LMAX = 16
WINDOW = 7
PASSES = 15
MASKMOD = 1073741823

letters = [0] * (WORDS * LMAX)
lens = [0] * WORDS
masks = [0] * WORDS
best = [0] * WORDS

seed = 318318


def next_rand() -> int:
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def write_word(w: int) -> None:
    ln = next_rand() % LMAX + 1
    base = next_rand() % (26 - WINDOW + 1)
    lens[w] = ln
    for k in range(ln):
        letters[w * LMAX + k] = base + next_rand() % WINDOW


def build_masks() -> None:
    for w in range(WORDS):
        m = 0
        for k in range(lens[w]):
            m |= 1 << letters[w * LMAX + k]
        masks[w] = m


def main() -> None:
    for w in range(WORDS):
        write_word(w)

    sink = 0
    for p in range(PASSES):
        write_word(p * 977 % WORDS)
        build_masks()

        for i in range(WORDS):
            best[i] = 0
        for i in range(WORDS):
            mi = masks[i]
            li = lens[i]
            for j in range(i + 1, WORDS):
                if mi & masks[j] == 0:
                    q = li * lens[j]
                    if q > best[i]:
                        best[i] = q
                    if q > best[j]:
                        best[j] = q

        total = 0
        top = 0
        for i in range(WORDS):
            total += best[i]
            if best[i] > top:
                top = best[i]
        sink = (sink * 31 + total + top) % MASKMOD

    print(f"checksum {sink}")


if __name__ == "__main__":
    main()
