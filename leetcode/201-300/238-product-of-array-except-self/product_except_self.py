# LeetCode 238 — Product of Array Except Self (oracle mirror).
def product_except_self(nums):
    n = len(nums); out = [1] * n
    prefix = 1
    for i in range(n):
        out[i] = prefix; prefix *= nums[i]
    suffix = 1
    for j in range(n - 1, -1, -1):
        out[j] *= suffix; suffix *= nums[j]
    return out

def report(nums):
    print(" ".join(str(x) for x in product_except_self(nums)))

for arr in ([1,2,3,4], [-1,1,0,-3,3], [2,3,4], [5,9]):
    report(arr)
