# Benchmark for #645: mirror of set_mismatch.kara (the ★ arm: counting
# each value) on the same workload.


def find_error_nums(nums):
    n = len(nums)
    seen = [0] * (n + 1)
    for x in nums:
        seen[x] += 1
    twice = 0
    missing = 0
    for v in range(1, n + 1):
        if seen[v] == 2:
            twice = v
        elif seen[v] == 0:
            missing = v
    return [twice, missing]


def main():
    seed = 645

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def mismatched(n):
        nums = list(range(1, n + 1))
        for i in range(n - 1):
            j = i + next_random() % (n - i)
            nums[i], nums[j] = nums[j], nums[i]
        frm = next_random() % n
        to = next_random() % (n - 1)
        if to >= frm:
            to += 1
        nums[to] = nums[frm]
        return nums

    arrays = [mismatched(100000) for _ in range(20)]
    rounds = 2000
    twice_sum = 0
    missing_sum = 0
    for r in range(rounds):
        got = find_error_nums(arrays[r % 20])
        twice_sum += got[0]
        missing_sum += got[1]
    print(f"{rounds} rounds over 20 arrays of 100000 values: copies add to {twice_sum}, missing values to {missing_sum}")


main()
