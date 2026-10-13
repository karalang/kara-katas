# LeetCode #540: Single Element in a Sorted Array -- Python mirror of
# the ★ arm (binary search over the pairs); see single_non_duplicate.kara.


def single_non_duplicate(nums):
    low, high = 0, len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if mid % 2 == 1:
            mid -= 1
        if nums[mid] == nums[mid + 1]:
            low = mid + 2
        else:
            high = mid
    return nums[low]


# ---- test harness ---------------------------------------------------------

seed = 540


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, nums):
    print(f"{name}: [{', '.join(map(str, nums))}] -> {single_non_duplicate(nums)}")


def array(pairs, single, top):
    values = []
    need = pairs + 1
    left = top + 1
    v = 0
    while need > 0:
        if (next_random() * 32768 + next_random()) % left < need:
            values.append(v)
            need -= 1
        left -= 1
        v += 1
    nums = []
    for i, x in enumerate(values):
        nums.append(x)
        if i != single:
            nums.append(x)
    return nums


def main():
    show("example 1", [1, 1, 2, 3, 3, 4, 4, 8, 8])
    show("example 2", [3, 3, 7, 7, 10, 11, 11])
    show("one element", [5])
    show("single first", [0, 1, 1, 2, 2])
    show("single last", [0, 0, 1, 1, 100000])
    show("single in the middle", [2, 2, 4, 6, 6])
    show("both ends of the range", [0, 0, 100000])
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        pairs = next_random() % 31
        single = next_random() % (pairs + 1)
        nums = array(pairs, single, 99)
        total += len(nums)
        checksum = (checksum * 31 + single_non_duplicate(nums) + 1) % 1000000007
    print(f"{count} random arrays: {total} elements, checksum {checksum}")
    for single in [0, 12500, 25000, 49999]:
        nums = array(49999, single, 100000)
        print(f"{len(nums)} elements, single at place {single}: {single_non_duplicate(nums)}")


main()
