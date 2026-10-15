# Benchmark for #643: mirror of max_average.kara (the ★ arm: a sliding
# sum) on the same workload.


def find_max_average(nums, k):
    s = 0
    for i in range(k):
        s += nums[i]
    best = s
    for i in range(k, len(nums)):
        s += nums[i] - nums[i - k]
        if s > best:
            best = s
    return best / k


def main():
    seed = 643
    arrays = []
    for _ in range(20):
        nums = []
        for _ in range(100000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append(seed // 65536 % 20001 - 10000)
        arrays.append(nums)
    rounds = 4000
    total = 0.0
    for r in range(rounds):
        k = 1 + (r * 7919) % 100000
        total += find_max_average(arrays[r % 20], k)
    print(f"{rounds} rounds over 20 arrays of 100000 values: answers adding to {total:.5f}")


main()
