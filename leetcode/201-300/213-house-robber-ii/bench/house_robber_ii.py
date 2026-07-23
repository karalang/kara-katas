"""Benchmark workload for LeetCode #213 — House Robber II (Python; scale lane)."""


def rob_linear(nums, lo, hi):
    prev = 0
    cur = 0
    for i in range(lo, hi):
        take = prev + nums[i]
        nxt = take if take > cur else cur
        prev = cur
        cur = nxt
    return cur


def rob_window(nums, s, w):
    if w == 1:
        return nums[s]
    skip_last = rob_linear(nums, s, s + w - 1)
    skip_first = rob_linear(nums, s + 1, s + w)
    return skip_last if skip_last > skip_first else skip_first


def main():
    n = 100000
    window = 2000
    windows = 130000

    nums = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        nums.append(1 + state % 1000)  # 1..1000, all positive

    span = n - window
    sink = 0
    for w in range(windows):
        s = (w * 977) % span
        sink += rob_window(nums, s, window)

    print(sink)


main()
