"""LeetCode 169 — Majority Element benchmark kernel (Python mirror).

Build-once + punch: LCG-filled N values with a 60% majority, Boyer-Moore scan run
K times with a one-element perturbation each round. Sink = sum of the K results.
Identical algorithm to the Kāra / C / Rust / Go mirrors.
"""


def majority_element(nums):
    candidate = nums[0]
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
        if x == candidate:
            count += 1
        else:
            count -= 1
    return candidate


def main():
    n = 10000000
    k = 20
    majority = 7
    nums = [0] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        if state % 100 < 60:
            nums[i] = majority
        else:
            nums[i] = state % 1000000 + 1000
    sink = 0
    for round in range(k):
        idx = (round * 7919) % n
        nums[idx] = nums[idx] + 1
        sink += majority_element(nums)
    print(sink)


main()
