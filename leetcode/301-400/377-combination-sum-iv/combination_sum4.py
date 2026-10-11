# LeetCode #377: Combination Sum IV -- mirror of combination_sum4.kara.
CAP = 1 << 31


def combination_sum4(nums, target):
    dp = [0] * (target + 1)
    dp[0] = 1
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                dp[t] = min(dp[t] + dp[t - x], CAP)
    return dp[target]


def show(label, nums, target):
    print(f"{label}: {combination_sum4(nums, target)}")


def main():
    show("example 1", [1, 2, 3], 4)
    show("example 2", [9], 3)
    show("target below every value", [5, 6, 7], 4)
    show("one value that divides", [4], 1000)
    show("one value that does not", [3], 1000)
    show("ones and twos to 40", [1, 2], 40)
    show("evens to an odd target", [2, 4], 999)
    show("3, 33, 333 to 1000", [3, 33, 333], 1000)
    show("large values", [997, 998, 999, 1000], 1000)
    # Half the cases use small values and a target up to 30; the other
    # half use values from 10 to 199 and a target that is a sum of one to
    # five of them, so it can always be reached. Every answer is below
    # 2^31, as the problem promises.
    seed = 377
    checksum = 0
    for case in range(200):
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = 1 + (seed // 65536) % 6
        lo, span = (1, 15) if case % 2 == 0 else (10, 190)
        nums = []
        while len(nums) < k:
            seed = (seed * 1103515245 + 12345) % 2147483648
            v = lo + (seed // 65536) % span
            if v not in nums:
                nums.append(v)
        seed = (seed * 1103515245 + 12345) % 2147483648
        if case % 2 == 0:
            target = 1 + (seed // 65536) % 30
        else:
            parts = 1 + (seed // 65536) % 5
            target = 0
            for _ in range(parts):
                seed = (seed * 1103515245 + 12345) % 2147483648
                target += nums[(seed // 65536) % k]
        checksum = (checksum * 1009 + combination_sum4(nums, target)) % 1000000007
    print(f"200 random cases: checksum {checksum}")


main()
