# Benchmark: LeetCode #1099 Two Sum Less Than K -- Python mirror of
# two_sum_less_than_k.kara: the ★ arm, sorting and two pointers, over 64
# arrays of 100 values built once, 400 rounds each changing one value per
# array and asking for 8 values of k.


def two_sum_less_than_k(nums, k):
    v = sorted(nums)
    best = -1
    lo, hi = 0, len(v) - 1
    while lo < hi:
        s = v[lo] + v[hi]
        if s < k:
            best = max(best, s)
            lo += 1
        else:
            hi -= 1
    return best


seed = 1099


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(64):
        arrays.append([next_random() % 1000 + 1 for _ in range(100)])
    found = 0
    check = 0
    for rnd in range(400):
        for j, a in enumerate(arrays):
            at = (rnd * 7 + j * 13) % 100
            a[at] = (a[at] + rnd * 31) % 1000 + 1
            for q in range(8):
                k = (rnd * 97 + j * 61 + q * 251) % 2000 + 1
                best = two_sum_less_than_k(a, k)
                if best >= 0:
                    found += 1
                check = (check * 31 + best + 1) % 1000000007
    print(f"400 rounds over 64 arrays of 100 values: {found} of 204800 with a pair, checksum {check}")


main()
