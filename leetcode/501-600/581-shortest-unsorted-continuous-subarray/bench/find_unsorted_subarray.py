# Benchmark for #581: Python mirror of the ★ arm (two sweeps); see
# find_unsorted_subarray.kara.


def find_unsorted_subarray(nums):
    n = len(nums)
    largest = nums[0]
    end = -1
    for i in range(1, n):
        if nums[i] < largest:
            end = i
        else:
            largest = nums[i]
    smallest = nums[n - 1]
    start = 0
    for i in range(n - 2, -1, -1):
        if nums[i] > smallest:
            start = i
        else:
            smallest = nums[i]
    if end == -1:
        return 0
    return end - start + 1


# ---- benchmark ----------------------------------------------------------------

seed = 581


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random() * 32768
    return high + next_random()


def main():
    count = 100
    rounds = 600
    cases = []
    for _ in range(count):
        nums = [wide() % 200001 - 100000 for _ in range(10000)]
        nums.sort()
        swaps = 1 + next_random() % 3
        for _ in range(swaps):
            i = wide() % 10000
            j = wide() % 10000
            nums[i], nums[j] = nums[j], nums[i]
        cases.append(nums)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            p = (rnd * 7 + g) % count
            got = find_unsorted_subarray(cases[p])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} arrays of 10000 values, {rounds} rounds: total {total}, checksum {checksum}")


main()
