# LeetCode #2441: Largest Positive Integer That Exists With Its Negative
# -- the bench, the ★ arm: a table of 2001 flags, offset by 1000, and the
# largest magnitude whose negative was seen.


def find_max_k(nums):
    seen = [False] * 2001
    best = -1
    for x in nums:
        if seen[1000 - x]:
            best = max(best, abs(x))
        seen[1000 + x] = True
    return best


seed = 2441


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def nonzero():
    v = 1 + next_random() % 1000
    return v if next_random() % 2 == 0 else -v


def main():
    arrays = [[nonzero() for _ in range(1000)] for _ in range(100)]
    check = 0
    for p in range(1000):
        for c in range(len(arrays)):
            at = (p * 7919 + c * 104729) % 1000
            arrays[c][at] = nonzero()
            check = (check * 31 + find_max_k(arrays[c]) + p) % 1000000007
    print(f"1000 passes over 100 arrays of 1000 values: checksum {check}")


main()
