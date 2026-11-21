# LeetCode #1658: Minimum Operations to Reduce X to Zero -- the Python
# mirror of the ★ arm: the longest middle summing to the total less x,
# found by a sliding window.


def min_operations(nums, x):
    target = sum(nums) - x
    if target < 0:
        return -1
    n = len(nums)
    longest = -1
    s = 0
    left = 0
    for right in range(n):
        s += nums[right]
        while s > target:
            s -= nums[left]
            left += 1
        if s == target:
            longest = max(longest, right - left + 1)
    return -1 if longest < 0 else n - longest


# ---- the harness: the same as every arm's ---------------------------------

seed = 1658


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, top):
    check = 0
    total = 0
    impossible = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        nums = [next_random() % top + 1 for _ in range(n)]
        if next_random() % 2 == 0:
            left = next_random() % (n + 1)
            right = next_random() % (n - left + 1)
            x = max(sum(nums[:left]) + sum(nums[n - right:]), 1)
        else:
            x = (next_random() * 32768 + next_random()) % (top * n) + 1
        answer = min_operations(nums, x)
        if answer < 0:
            impossible += 1
        total += answer
        check = (check * 31 + answer + 2) % 1000000007
    print(f"{count} arrays of up to {most} numbers to {top}: operations sum to {total}, {impossible} impossible, checksum {check}")


print(min_operations([1, 1, 4, 2, 3], 5))
print(min_operations([5, 6, 7, 8, 9], 4))
print(min_operations([3, 2, 20, 1, 1, 3], 10))
print(min_operations([2, 3, 4], 9))
print(min_operations([7, 1, 1], 7))
print(min_operations([1, 2], 4))
batch(3000, 10, 5)
batch(1000, 1000, 10000)
batch(20, 100000, 10000)
