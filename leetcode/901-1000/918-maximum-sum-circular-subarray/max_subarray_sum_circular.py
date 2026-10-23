# LeetCode #918: Maximum Sum Circular Subarray -- Python mirror of Kadane
# for the largest and the smallest sum in max_subarray_sum_circular.kara,
# with its harness.


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


def show(nums):
    print(f"[{','.join(str(v) for v in nums)}]: {max_subarray_sum_circular(nums)}")


def random_values(n, lean):
    nums = []
    for _ in range(n):
        high = next_random()
        v = (high * 2 + next_random() % 2) % 60001 - 30000 + lean
        nums.append(min(max(v, -30000), 30000))
    return nums


def main():
    for nums in [[1, -2, 3, -2], [5, -3, 5], [-3, -2, -3], [3, -1, 2, -1], [3, -2, 2, -3], [-2, -3, -1],
                 [1], [-5], [0, 0, 0], [2, -1, 2], [-1, 5, -1, -1, 5, -1]]:
        show(nums)
    total = 0
    check = 0
    for c in range(500):
        n = 1 + next_random() % 1000
        lean = (c % 7 - 3) * 5000
        r = max_subarray_sum_circular(random_values(n, lean))
        total += r
        check = (check * 1000003 + r + 1000000000) % 1000000007
    print(f"500 arrays: answers summing to {total}, checksum {check}")
    print(f"30000 values of -30000: {max_subarray_sum_circular([-30000] * 30000)}")
    print(f"30000 values of 30000: {max_subarray_sum_circular([30000] * 30000)}")
    print(f"30000 random values: {max_subarray_sum_circular(random_values(30000, 0))}")
    valley = [-30000 + i % 7 if 10000 <= i < 20000 else 30000 - i % 11 for i in range(30000)]
    print(f"30000 values with a valley: {max_subarray_sum_circular(valley)}")


main()
