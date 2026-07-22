"""Benchmark workload — Maximum Product Subarray, O(n) running max/min DP.
Algorithmic mirror of bench/max_product.kara / .c / .rs / go-seq."""


def max_product(nums):
    if not nums:
        return 0
    best = cur_max = cur_min = nums[0]
    for x in nums[1:]:
        if x < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(x, cur_max * x)
        cur_min = min(x, cur_min * x)
        if cur_max > best:
            best = cur_max
    return best


def main():
    N = 2_000_000
    data = [0] * N
    state = 12345
    for i in range(N):
        state = (state * 1103515245 + 12345) & 2147483647
        data[i] = (state % 5) - 2
    total = 0
    for _ in range(10):
        total += max_product(data)
    print(total)


main()
