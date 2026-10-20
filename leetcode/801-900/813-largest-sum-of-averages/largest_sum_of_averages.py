# LeetCode 813 — Largest Sum of Averages, one row of prefix-sum DP (mirror of the ★ arm).


def largest_sum_of_averages(nums, k):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    best = [0.0] * (n + 1)
    for i in range(1, n + 1):
        best[i] = prefix[i] / i
    for _ in range(1, k):
        i = n
        while i >= 1:
            for p in range(1, i):
                candidate = best[p] + (prefix[i] - prefix[p]) / (i - p)
                if candidate > best[i]:
                    best[i] = candidate
            i -= 1
    return best[n]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, k):
    print(f"nums = {nums}, k = {k} -> {largest_sum_of_averages(nums, k):.5f}")


def main():
    global seed
    show([9, 1, 2, 3, 9], 3)
    show([1, 2, 3, 4, 5, 6, 7], 4)
    show([5], 1)
    show([4, 1, 7], 1)
    show([4, 1, 7], 3)
    show([1, 1, 1, 1], 2)
    show([1, 1, 10000, 1], 2)
    show([3, 10, 3, 10, 3], 2)
    seed = 813
    big = [1 + next_random() % 10000 for _ in range(100)]
    for k in [1, 7, 50, 100]:
        print(f"100 numbers, k = {k} -> {largest_sum_of_averages(big, k):.5f}")
    total = 0.0
    for _ in range(300):
        n = 1 + next_random() % 12
        nums = [1 + next_random() % 50 for _ in range(n)]
        k = 1 + next_random() % n
        total += largest_sum_of_averages(nums, k)
    print(f"300 random rounds of 1 to 12 numbers: total {total:.5f}")


main()
