# Bench for LeetCode #354 -- Python mirror of russian_doll.kara: sort by width
# ascending and height descending, then a patience-sorting LIS over heights.

ROUNDS = 20
COUNT = 200000


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


def main():
    sink = 0
    for rnd in range(ROUNDS):
        seed = 354 + rnd
        envelopes = []
        for _ in range(COUNT):
            seed = (seed * 1103515245 + 12345) % 2147483648
            w = seed % 100000 + 1
            seed = (seed * 1103515245 + 12345) % 2147483648
            h = seed % 100000 + 1
            envelopes.append((w, h))
        sink = (sink * 31 + max_envelopes(envelopes) + rnd) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
