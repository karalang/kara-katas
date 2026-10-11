# Benchmark for #377: mirror of combination_sum4.kara.
CAP = 1 << 31


def combination_sum4(nums, target):
    ways = [0] * (target + 1)
    ways[0] = 1
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                ways[t] = min(ways[t] + ways[t - x], CAP)
    return ways[target]


def main():
    seed = 377
    checksum = 0
    for _ in range(2000):
        nums = []
        while len(nums) < 200:
            seed = (seed * 1103515245 + 12345) % 2147483648
            v = 125 + (seed // 65536) % 875
            if v not in nums:
                nums.append(v)
        checksum = (checksum * 1009 + combination_sum4(nums, 1000)) % 1000000007
    print(f"checksum {checksum}")


main()
