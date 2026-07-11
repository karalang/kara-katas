"""Benchmark workload — Subsets II (LeetCode #90).

Python mirror of bench/subsets_ii.kara. Enumerate-and-fold over the emit-at-node dedup
backtracking of a sorted multiset (8 distinct values x2 => 3^8 unique subsets). Smaller
K (pure-Python recursion is slow); timed separately, NOT cross-checked. See ../README.md.
"""


def enumerate_subsets(nums, start, path, acc):
    a = (acc * 131 + (len(path) + 1)) % 1000000007
    for x in path:
        a = (a * 131 + (x + 1)) % 1000000007
    n = len(nums)
    i = start
    while i < n:
        if i == start or nums[i] != nums[i - 1]:
            path.append(nums[i])
            a = enumerate_subsets(nums, i + 1, path, a)
            path.pop()
        i += 1
    return a


def main():
    d, r = 8, 2
    total = 300
    modulus = 1000000007
    nums = []
    for v in range(d):
        for _ in range(r):
            nums.append(v)
    total_sum = 0
    for it in range(total):
        rr = enumerate_subsets(nums, 0, [], it)
        total_sum = (total_sum * 131 + rr) % modulus
    print(total_sum)


if __name__ == "__main__":
    main()
