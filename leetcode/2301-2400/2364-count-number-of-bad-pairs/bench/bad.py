# LeetCode #2364: Count Number of Bad Pairs -- the bench, the ★ arm in
# Python: each place's key nums[j] - j counted in a dict as the places go
# by, the places before j with the same key its good pairs, and the bad
# pairs all n (n - 1) / 2 less the good ones.


def count_bad_pairs(nums):
    n = len(nums)
    seen = {}
    good = 0
    for j in range(n):
        key = nums[j] - j
        before = seen.get(key, 0)
        good += before
        seen[key] = before + 1
    return n * (n - 1) // 2 - good


SEED = [2364]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    # array a: 10^5 values, each the place plus one of 4^a offsets (at
    # most 10^5) below 999 * 10^6, so the keys run from one to tens of
    # thousands
    arrays = []
    for a in range(10):
        kinds = 1 << (2 * a)
        offsets = [wide_random() % 999000000 for _ in range(min(kinds, 100000))]
        arrays.append([1 + i + offsets[wide_random() % len(offsets)] for i in range(100000)])
    check = 0
    for p in range(20):
        for nums in arrays:
            check = (check * 31 + count_bad_pairs(nums) % 1000000007 + p) % 1000000007
    print(f"20 passes over 10 arrays of 10^5 values: checksum {check}")


main()
