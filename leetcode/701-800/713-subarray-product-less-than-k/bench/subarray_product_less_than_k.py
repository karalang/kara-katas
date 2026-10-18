# LeetCode #713: Subarray Product Less Than K -- a sliding window.
# Benchmark mirror of the Kara star arm: extend the window right; while
# its product is k or more, drop numbers from the left; count the
# subarrays ending at each right end.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def num_subarray_product_less_than_k(nums, k):
    if k <= 1:
        return 0
    product = 1
    left = 0
    count = 0
    for right in range(len(nums)):
        product *= nums[right]
        while product >= k:
            product //= nums[left]
            left += 1
        count += right - left + 1
    return count


def main():
    seed = [713]
    tops = [2, 3, 5, 10, 20, 50, 100, 200, 500, 1000]
    arrays = [[1 + next_random(seed) % t for _ in range(30000)] for t in tops]
    total = 0
    for _ in range(200):
        for nums in arrays:
            total += num_subarray_product_less_than_k(nums, 1000000)
    print(f"200 rounds of 10 arrays of 30000, k = 1000000: sum {total}")


main()
