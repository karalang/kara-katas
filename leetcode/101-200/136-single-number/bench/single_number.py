"""Benchmark workload for LeetCode #136 — Single Number (Python; scale lane)."""


def single_number(nums, n):
    acc = 0
    for i in range(n):
        acc ^= nums[i]
    return acc


def main():
    pairs = 140000
    passes = 3400
    n = 2 * pairs + 1

    nums = []
    state = 12345
    for _ in range(pairs):
        state = (state * 1103515245 + 12345) & 2147483647
        v = state >> 16
        nums.append(v)
        nums.append(v)
    state = (state * 1103515245 + 12345) & 2147483647
    nums.append(state >> 16)

    sink = 0
    for p in range(passes):
        idx = (p * 97 + 13) % n
        nums[idx] ^= 1 << (p % 14)
        sink += single_number(nums, n)
    print(sink)


main()
