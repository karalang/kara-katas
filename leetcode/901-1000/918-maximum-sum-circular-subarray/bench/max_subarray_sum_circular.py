# LeetCode #918: Maximum Sum Circular Subarray -- bench: Python mirror of
# Kadane for the largest and the smallest sum in
# max_subarray_sum_circular.kara.


def max_subarray_sum_circular(nums):
    total = 0
    best_here = 0
    best = nums[0]
    worst_here = 0
    worst = nums[0]
    for v in nums:
        total += v
        best_here = max(v, best_here + v)
        best = max(best, best_here)
        worst_here = min(v, worst_here + v)
        worst = min(worst, worst_here)
    if best < 0:
        return best
    return max(best, total - worst)


seed = 918


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def value():
    high = next_random()
    return (high * 2 + next_random() % 2) % 60001 - 30000


def main():
    rounds = 4000
    n = 30000
    nums = [value() for _ in range(n)]
    total = 0
    check = 0
    for _ in range(rounds):
        i = next_random() % n
        old = nums[i]
        nums[i] = value()
        r = max_subarray_sum_circular(nums)
        total += r
        check = (check * 1000003 + r) % 1000000007
        nums[i] = old
    print(f"{rounds} rounds over {n} values: answers summing to {total}, checksum {check}")


main()
