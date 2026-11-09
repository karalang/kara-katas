# LeetCode #2035: Partition Array Into Two Arrays to Minimize Sum Difference
# -- a Python mirror of the ★ arm (partition.kara): meet in the middle, the
# subset sums of each half listed by size, the right lists sorted, and a
# binary search for the right sum nearest half the total.
from bisect import bisect_left


def subset_sums(half):
    n = len(half)
    by_size = [[] for _ in range(n + 1)]
    for mask in range(1 << n):
        s = size = 0
        for i in range(n):
            if mask >> i & 1 == 1:
                s += half[i]
                size += 1
        by_size[size].append(s)
    return by_size


def minimum_difference(nums):
    n = len(nums) // 2
    total = sum(nums)
    left = subset_sums(nums[:n])
    right = subset_sums(nums[n:])
    for lst in right:
        lst.sort()
    best = None
    for k in range(n + 1):
        others = right[n - k]
        keys = [2 * b for b in others]
        for a in left[k]:
            # first b with 2 (a + b) >= total
            at = bisect_left(keys, total - 2 * a)
            if at < len(others):
                d = abs(total - 2 * (a + others[at]))
                best = d if best is None else min(best, d)
            if at > 0:
                d = abs(total - 2 * (a + others[at - 1]))
                best = d if best is None else min(best, d)
    return best


seed = 2035


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer % 1000000007) % 1000000007


def random_values(n, top):
    return [(next_random() * 32768 + next_random()) % (2 * top + 1) - top for _ in range(2 * n)]


def main():
    examples = [
        [3, 9, 7, 3],
        [-36, 36],
        [2, -1, 0, 4, -2, -9],
        [5, 5],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [10000000, -10000000, 10000000, -10000000],
        [0, 0, 0, 0, 0, 1],
        [7, -3, 12, 1, -8, 4, 9, -11, 2, 6],
    ]
    for nums in examples:
        print(f"{nums} -> {minimum_difference(nums)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 6 + 1
        top = next_random() % 50 + 1
        answer = minimum_difference(random_values(n, top))
        total += answer
        check = mix(check, answer)
    print(f"2000 arrays of up to 12 values: sum {total}, checksum {check}")
    total = check = 0
    for a in range(4):
        top = [10000000, 1000, 10000000, 3][a]
        answer = minimum_difference(random_values(15, top))
        total += answer
        check = mix(check, answer)
    print(f"4 arrays of 30 values: sum {total}, checksum {check}")


main()
