# LeetCode #1671: Minimum Number of Removals to Make Mountain Array -- the
# bench's Python mirror: the ★ arm on 300 arrays of 1000 values up to
# 10^9, one raised above the rest, all drawn first.


def minimum_mountain_removals(nums):
    n = len(nums)
    up = [1] * n
    down = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                up[i] = max(up[i], up[j] + 1)
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:
                down[i] = max(down[i], down[j] + 1)
    longest = 0
    for i in range(1, n - 1):
        if up[i] > 1 and down[i] > 1:
            longest = max(longest, up[i] + down[i] - 1)
    return n - longest


# ---- the harness ----------------------------------------------------------

seed = 1671


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


arrays = 300
n = 1000
most = 1000000000
all_nums = []
for _ in range(arrays):
    nums = [(next_random() * 32768 + next_random()) % most + 1 for _ in range(n)]
    peak = next_random() % (n - 2) + 1
    nums[peak] = most + 1
    all_nums.append(nums)
total = 0
check = 0
for nums in all_nums:
    removed = minimum_mountain_removals(nums)
    total += removed
    check = (check * 31 + removed) % 1000000007
print(f"{arrays} arrays of {n} values: {total} removals, checksum {check}")
