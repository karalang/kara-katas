# LeetCode #2763: Sum of Imbalance Numbers of All Subarrays -- the ★ arm
# in Python (imbalance.kara): a subarray's imbalance is its count of runs
# of consecutive values, less 1, and a run is counted once, at the
# leftmost occurrence of its top value x with no x + 1 in the subarray.
# Each index i is that for (i - left) (right - i) subarrays, left the last
# x or x + 1 before it and right the first x + 1 after it.


def sum_imbalance_numbers(nums):
    n = len(nums)
    left = [0] * n
    last = [-1] * (n + 2)
    for i, x in enumerate(nums):
        left[i] = max(last[x], last[x + 1])
        last[x] = i
    total = 0
    first = [n] * (n + 2)
    for i in range(n - 1, -1, -1):
        x = nums[i]
        total += (i - left[i]) * (first[x + 1] - i)
        first[x] = i
    return total - n * (n + 1) // 2


seed = 2763


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(sum_imbalance_numbers([2, 3, 1, 4]))
    print(sum_imbalance_numbers([1, 3, 3, 3, 5]))
    print(sum_imbalance_numbers([1]))
    print(sum_imbalance_numbers([1] * 1000))
    print(sum_imbalance_numbers(list(range(1, 1001))))
    print(sum_imbalance_numbers([1000 - 2 * (i % 500) for i in range(1000)]))
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 20 + 1
        nums = [next_random() % n + 1 for _ in range(n)]
        a = sum_imbalance_numbers(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 small arrays: imbalances sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(5):
        nums = [next_random() % 1000 + 1 for _ in range(1000)]
        a = sum_imbalance_numbers(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"5 arrays of 1000: imbalances sum to {total}, checksum {check}")


main()
