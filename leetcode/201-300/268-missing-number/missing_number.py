# LeetCode 268 — Missing Number (oracle mirror).
def missing_number(nums):
    acc = len(nums)
    for i, v in enumerate(nums): acc ^= i ^ v
    return acc
for arr in ([3,0,1], [0,1], [9,6,4,2,3,5,7,0,1], [0], [1]):
    print(missing_number(arr))
