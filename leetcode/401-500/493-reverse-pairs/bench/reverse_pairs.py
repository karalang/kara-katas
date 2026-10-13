# Benchmark for #493: Python mirror of the ★ arm (merge sort); see
# reverse_pairs.kara.


def sort_count(nums, low, high):
    if high - low <= 1:
        return 0
    mid = (low + high) // 2
    count = sort_count(nums, low, mid) + sort_count(nums, mid, high)
    j = mid
    for i in range(low, mid):
        while j < high and nums[i] > 2 * nums[j]:
            j += 1
        count += j - mid
    merged = []
    a, b = low, mid
    while a < mid or b < high:
        if b == high or (a < mid and nums[a] <= nums[b]):
            merged.append(nums[a])
            a += 1
        else:
            merged.append(nums[b])
            b += 1
    nums[low:high] = merged
    return count


def reverse_pairs(nums):
    work = list(nums)
    return sort_count(work, 0, len(work))


def main():
    # 60 arrays of 50,000 numbers across the whole 32-bit range, built
    # once, then each counted once.
    seed = 493

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(60):
        nums = []
        for _ in range(50000):
            high = next_random()
            nums.append(high * 131072 + next_random() * 4 - 2147483648)
        arrays.append(nums)
    total = 0
    checksum = 0
    for nums in arrays:
        pairs = reverse_pairs(nums)
        total += pairs
        checksum = (checksum * 31 + pairs) % 1000000007
    print(f"60 arrays of 50000: {total} reverse pairs, checksum {checksum}")


main()
