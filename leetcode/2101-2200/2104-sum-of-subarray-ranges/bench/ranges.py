# LeetCode #2104: Sum of Subarray Ranges -- bench, Python mirror of
# ranges.kara.


def sub_array_ranges(nums):
    n = len(nums)
    total = 0
    stack = []
    for i in range(n + 1):
        while stack and (i == n or nums[stack[-1]] < nums[i]):
            top = stack.pop()
            left = stack[-1] if stack else -1
            total += nums[top] * (top - left) * (i - top)
        stack.append(i)
    stack.clear()
    for i in range(n + 1):
        while stack and (i == n or nums[stack[-1]] > nums[i]):
            top = stack.pop()
            left = stack[-1] if stack else -1
            total -= nums[top] * (top - left) * (i - top)
        stack.append(i)
    return total


seed = 2104


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


arrays = [[wide_random() % 2000000001 - 1000000000 for _ in range(1000)] for _ in range(1000)]
total = 0
check = 0
for _ in range(10):
    for nums in arrays:
        got = sub_array_ranges(nums) % 1000000007
        total = (total + got) % 1000000007
        check = (check * 31 + got) % 1000000007
print(f"10000 arrays: total {total}, checksum {check}")
