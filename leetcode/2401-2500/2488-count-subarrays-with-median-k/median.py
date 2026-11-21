# LeetCode #2488: Count Subarrays With Median K -- Python mirror of the ★
# arm (median.kara): the balances of the starts left of `k` counted in a
# dict, and each end right of it adding the starts that make 0 or 1.


def count_subarrays(nums, k):
    n = len(nums)
    at = nums.index(k)
    starts = {0: 1}
    balance = 0
    for i in range(at - 1, -1, -1):
        balance += 1 if nums[i] > k else -1
        starts[balance] = starts.get(balance, 0) + 1
    count = 0
    balance = 0
    for j in range(at, n):
        if j > at:
            balance += 1 if nums[j] > k else -1
        count += starts.get(-balance, 0) + starts.get(1 - balance, 0)
    return count


# ---- test harness -----------------------------------------------------------

seed = 2488


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def permutation(n):
    nums = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = (next_random() * 32768 + next_random()) % (i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [
        ([3, 2, 1, 4, 5], 4),
        ([2, 3, 1], 3),
        ([1], 1),
        ([1, 2], 1),
        ([2, 1], 2),
        ([1, 2, 3], 2),
        ([5, 1, 4, 2, 3], 3),
        ([4, 1, 7, 3, 6, 2, 5], 4),
    ]
    for nums, k in cases:
        print(f"{show(nums)}, {k} -> {count_subarrays(nums, k)}")
    check = 0
    for _ in range(2000):
        n = next_random() % 200 + 1
        nums = permutation(n)
        k = next_random() % n + 1
        check = (check * 31 + count_subarrays(nums, k)) % 1000000007
    print(f"2000 random: checksum {check}")
    n = 100000
    rising = list(range(1, n + 1))
    falling = list(range(n, 0, -1))
    random = permutation(n)
    for name, nums in [("rising", rising), ("falling", falling), ("random", random)]:
        for k in [1, n // 2, n]:
            print(f"10^5 {name}, {k} -> {count_subarrays(nums, k)}")


main()
