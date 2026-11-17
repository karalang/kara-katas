# LeetCode #1182: Maximum Subarray Sum with One Deletion -- the ★ arm in
# Python: one pass carrying the best sum ending here with nothing deleted
# (`kept`) and with one element deleted (`cut`).

MIN = -(1 << 63)


def maximum_sum(arr):
    kept = arr[0]
    cut = MIN
    best = arr[0]
    for x in arr[1:]:
        cut = kept if cut == MIN else max(cut + x, kept)
        kept = max(kept + x, x)
        best = max(best, kept, cut)
    return best


def main():
    seed = 1182

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = [[next_random() % 20001 - 10000 for _ in range(100000)] for _ in range(10)]
    rounds = 100
    check = 0
    for r in range(rounds):
        for arr in arrays:
            check = (check * 131 + maximum_sum(arr) + r) % 1000000007
    print(f"{rounds} rounds of 10 arrays: checksum {check}")


main()
