# LeetCode #2134: Minimum Swaps to Group All 1's Together II -- the mirror
# of swaps.kara: k less the most 1s a window of k holds, the window slid
# once round the circle by index mod n.


def min_swaps(nums):
    n = len(nums)
    k = sum(nums)
    inside = 0
    for i in range(k):
        inside += nums[i]
    most = inside
    for i in range(k, n + k):
        inside += nums[i % n] - nums[(i - k) % n]
        most = max(most, inside)
    return k - most


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(nums):
    print(f"[{', '.join(str(v) for v in nums)}] -> {min_swaps(nums)}")


def main():
    show([0, 1, 0, 1, 1, 0, 0])
    show([0, 1, 1, 1, 0, 0, 1, 1, 0])
    show([1, 1, 0, 0, 1])
    show([0])
    show([1])
    show([1, 0, 1, 0, 1, 0])
    show([0, 0, 0])
    seed = [2134]
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random(seed) % 12 + 1
        k = [2, 3, 5][rnd % 3]
        nums = [1 if next_random(seed) % k == 0 else 0 for _ in range(n)]
        swaps = min_swaps(nums)
        total += swaps
        check = (check * 31 + swaps + n) % 1000000007
    print(f"2000 arrays: {total} swaps in all, checksum {check}")
    turns = [(i + 1) % 2 for i in range(100000)]
    ends = [1 if i < 30000 or i >= 70000 else 0 for i in range(100000)]
    rand = [next_random(seed) % 2 for _ in range(100000)]
    x = min_swaps(turns)
    y = min_swaps(ends)
    z = min_swaps(rand)
    print(f"100000 values: {x} in turn, {y} at the ends, {z} at random")


main()
