# LeetCode #354: Russian Doll Envelopes -- Python mirror of russian_doll.kara.
# Sort by width ascending, height descending; then a patience-sorting longest
# strictly increasing subsequence over the heights.


def max_envelopes(envelopes):
    order = sorted(envelopes, key=lambda e: (e[0], -e[1]))
    tails = []
    for _, h in order:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < h:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(h)
        else:
            tails[lo] = h
    return len(tails)


def show(label, envelopes):
    print(f"{label}: {max_envelopes(envelopes)}")


def main():
    show("example 1", [(5, 4), (6, 4), (6, 7), (2, 3)])
    show("example 2", [(1, 1), (1, 1), (1, 1)])
    show("one envelope", [(7, 7)])
    show("same width, rising heights", [(3, 1), (3, 2), (3, 3), (3, 4)])
    show("same height, rising widths", [(1, 5), (2, 5), (3, 5)])
    show("a clean chain", [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    show("a chain given backwards", [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)])
    show("wide but short", [(10, 1), (1, 10), (2, 2), (3, 3)])
    show("ties break the chain", [(1, 2), (2, 3), (2, 4), (3, 5), (3, 4), (4, 6)])
    seed = 12345
    big = []
    for _ in range(3000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        w = seed % 1500 + 1
        seed = (seed * 1103515245 + 12345) % 2147483648
        h = seed % 1500 + 1
        big.append((w, h))
    print(f"3000 random envelopes: {max_envelopes(big)}")


if __name__ == "__main__":
    main()
