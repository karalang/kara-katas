# LeetCode #2035: Partition Array Into Two Arrays to Minimize Sum
# Difference -- the ★ arm in Python, the same algorithm and workload as
# partition.kara: each half's subset sums listed by size, the right lists
# sorted, and a lower bound (the same predicate as `partition_point`) for
# the right sum that brings the side to half the total, with the sums on
# either side tried.


def subset_sums(half):
    n = len(half)
    by_size = [[] for _ in range(n + 1)]
    for mask in range(1 << n):
        s = 0
        size = 0
        for i in range(n):
            if mask >> i & 1 == 1:
                s += half[i]
                size += 1
        by_size[size].append(s)
    return by_size


def minimum_difference(nums):
    n = len(nums) // 2
    total = sum(nums)
    left = subset_sums(nums[0:n])
    right = subset_sums(nums[n:2 * n])
    for lst in right:
        lst.sort()
    best = None
    for k in range(n + 1):
        others = right[n - k]
        for a in left[k]:
            lo, hi = 0, len(others)
            while lo < hi:
                mid = (lo + hi) // 2
                if 2 * (a + others[mid]) < total:
                    lo = mid + 1
                else:
                    hi = mid
            at = lo
            if at < len(others):
                d = abs(total - 2 * (a + others[at]))
                best = d if best is None or d < best else best
            if at > 0:
                d = abs(total - 2 * (a + others[at - 1]))
                best = d if best is None or d < best else best
    return best


seed = 2035


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(40):
        top = [10000000, 1000, 100, 10000000, 50][a % 5]
        nums = []
        for _ in range(30):
            hi = next_random()
            lo = next_random()
            nums.append((hi * 32768 + lo) % (2 * top + 1) - top)
        arrays.append(nums)
    calls = 0
    total = 0
    check = 0
    for rnd in range(5):
        for a in range(40):
            at = (rnd * 7 + a * 3) % 30
            arrays[a][at] = -arrays[a][at]
            answer = minimum_difference(arrays[a])
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
