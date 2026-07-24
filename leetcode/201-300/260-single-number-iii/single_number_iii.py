# LeetCode 260 — Single Number III (oracle mirror).
def two_singles(nums):
    x = 0
    for v in nums: x ^= v
    bit = x & (-x)
    a = b = 0
    for v in nums:
        if v & bit: a ^= v
        else: b ^= v
    return sorted((a, b))
def report(nums):
    r = two_singles(nums); print(f"{r[0]} {r[1]}")
for arr in ([1,2,1,3,2,5], [-1,0], [0,1], [7,3,7,9,3,4,9,12], [-2,-2,5,8]):
    report(arr)
