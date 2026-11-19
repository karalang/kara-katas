# LeetCode #1658: Minimum Operations to Reduce X to Zero -- the bench's
# Python mirror: the ★ arm on 1000 random arrays of 100000 numbers from 1
# to 10000, each x a random prefix plus a random suffix of its array, all
# drawn first.


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


seed = 1658


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


n = 100000
problems = []
for _ in range(1000):
    nums = [next_random() % 10000 + 1 for _ in range(n)]
    left = next_random() % 1000
    right = next_random() % 1000
    x = sum(nums[:left]) + sum(nums[n - right:])
    problems.append((nums, max(x, 1)))
check = 0
total = 0
for nums, x in problems:
    answer = min_operations(nums, x)
    total += answer
    check = (check * 31 + answer + 2) % 1000000007
print(f"1000 arrays of 100000 numbers: operations sum to {total}, checksum {check}")
