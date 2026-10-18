# LeetCode #713: Subarray Product Less Than K -- a sliding window.
#
# A mirror of subarray_product_less_than_k.kara (the ★ arm) and its
# harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def show(nums, k):
    shown = "[" + ", ".join(str(x) for x in nums) + "]"
    print(f"{shown}, k = {k} -> {num_subarray_product_less_than_k(nums, k)}")


def main():
    global seed
    show([10, 5, 2, 6], 100)
    show([1, 2, 3], 0)
    show([1, 1, 1], 1)
    show([1, 1, 1], 2)
    show([5], 5)
    show([5], 6)
    show([2, 5, 10], 10)
    show([1000, 1000, 1000], 1000000)
    show([1000, 999, 1], 1000000)
    show([3, 3, 3, 3], 81)
    show([3, 3, 3, 3], 82)
    seed = 713
    ones = [1] * 3000
    print(f"3000 ones, k = 2: {num_subarray_product_less_than_k(ones, 2)}")
    small = [1 + next_random() % 3 for _ in range(30000)]
    a = num_subarray_product_less_than_k(small, 1000000)
    print(f"30000 of 1 to 3, k = 1000000: {a}")
    wide = [1 + next_random() % 1000 for _ in range(30000)]
    b = num_subarray_product_less_than_k(wide, 1000000)
    print(f"30000 of 1 to 1000, k = 1000000: {b}")
    total = 0
    for _ in range(500):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 20
        nums = [1 + next_random() % top for _ in range(n)]
        k = next_random() % 2000
        total = (total * 131
                 + num_subarray_product_less_than_k(nums, k)) % 1000000007
    print(f"500 random arrays: checksum {total}")


main()
