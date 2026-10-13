# LeetCode #493: Reverse Pairs -- Python mirror of the ★ arm (merge
# sort); see reverse_pairs.kara.


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


def show(name, nums):
    print(f"{name}: {nums} -> {reverse_pairs(nums)}")


seed = 493


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", [1, 3, 2, 3, 1])
    show("example 2", [2, 4, 3, 5, 1])
    show("one number", [7])
    show("rising", [1, 2, 3, 4, 5])
    show("falling", [16, 8, 4, 2, 1])
    show("exactly twice", [4, 2, 2, 1])
    show("negatives", [-5, -5, -3, -1, 0])
    show("the extremes", [2147483647, 2147483647, -2147483648, -2147483648])
    # 300 random arrays of 1 to 40 numbers, from -50 to 50 or across the
    # whole 32-bit range in turn.
    count = 300
    total = 0
    checksum = 0
    for c in range(count):
        size = 1 + next_random() % 40
        nums = []
        for _ in range(size):
            if c % 2 == 0:
                x = next_random() % 101 - 50
            else:
                high = next_random()
                x = high * 131072 + next_random() * 4 - 2147483648
            nums.append(x)
        pairs = reverse_pairs(nums)
        total += pairs
        checksum = (checksum * 31 + pairs) % 1000000007
    print(f"{count} random arrays: {total} reverse pairs, checksum {checksum}")


main()
