# LeetCode 239 — Sliding Window Maximum (oracle mirror).
from collections import deque
def max_sliding_window(nums, k):
    out = []; dq = deque()
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] <= v: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: out.append(nums[dq[0]])
    return out
def report(nums, k): print(" ".join(str(x) for x in max_sliding_window(nums, k)))
report([1,3,-1,-3,5,3,6,7], 3)
report([1], 1)
report([9,11], 2)
report([4,3,2,1,5,2], 2)
report([7,2,4,6,1], 5)
