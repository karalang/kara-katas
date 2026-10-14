# LeetCode #581: Shortest Unsorted Continuous Subarray -- two sweeps.
#
# Python mirror of find_unsorted_subarray.kara (the starred arm): the
# last place below the largest so far from the left is the end, the
# last place above the smallest so far from the right is the start.


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


# ---- test harness -----------------------------------------------------------

seed = 581


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"{nums}: {find_unsorted_subarray(nums)}")


def main():
    show([2, 6, 4, 8, 10, 9, 15])
    show([1, 2, 3, 4])
    show([1])
    show([2, 1])
    show([5, 5, 5, 5])
    show([5, 4, 3, 2, 1])
    show([100000, -100000])
    show([1, 3, 2, 2, 2])
    show([1, 2, 3, 3, 3, 2])
    show([2, 2, 1, 2, 2])
    show([1, 2, 3, 4, 5, 0, 6])
    show([1, 9, 2, 3, 4, 5, 6])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + step() % 30
        span = 1 + step() % 40
        nums = [step() % span - span // 2 for _ in range(n)]
        nums.sort()
        swaps = step() % 4
        for _ in range(swaps):
            i = step() % n
            j = step() % n
            nums[i], nums[j] = nums[j], nums[i]
        got = find_unsorted_subarray(nums)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random arrays: total {total}, checksum {checksum}")
    ends = [i * 20 - 100000 for i in range(10000)]
    ends[0], ends[9999] = ends[9999], ends[0]
    print(f"10000 values, the ends swapped: {find_unsorted_subarray(ends)}")
    middle = [i * 20 - 100000 for i in range(10000)]
    middle[4999], middle[5000] = middle[5000], middle[4999]
    print(f"10000 values, two in the middle swapped: {find_unsorted_subarray(middle)}")
    falling = [99999 - i * 20 for i in range(10000)]
    print(f"10000 values falling: {find_unsorted_subarray(falling)}")


main()
