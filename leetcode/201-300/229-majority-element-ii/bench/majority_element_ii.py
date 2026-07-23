"""Benchmark workload for LeetCode #229 — Majority Element II (Python; scale lane)."""


def window_majority_sum(nums, s, win):
    cand1 = cand2 = 0
    count1 = count2 = 0
    end = s + win
    k = s
    while k < end:
        x = nums[k]
        if count1 > 0 and x == cand1:
            count1 += 1
        elif count2 > 0 and x == cand2:
            count2 += 1
        elif count1 == 0:
            cand1 = x
            count1 = 1
        elif count2 == 0:
            cand2 = x
            count2 = 1
        else:
            count1 -= 1
            count2 -= 1
        k += 1

    real1 = real2 = 0
    j = s
    while j < end:
        x = nums[j]
        if count1 > 0 and x == cand1:
            real1 += 1
        elif count2 > 0 and x == cand2:
            real2 += 1
        j += 1

    threshold = win // 3
    total = 0
    if count1 > 0 and real1 > threshold:
        total += cand1
    if count2 > 0 and real2 > threshold:
        total += cand2
    return total


def main():
    n = 3000000
    win = 16

    nums = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        nums.append((state % 3) + 1)

    sink = 0
    last = n - win
    s = 0
    while s <= last:
        sink += window_majority_sum(nums, s, win)
        s += 1
    print(sink)


main()
