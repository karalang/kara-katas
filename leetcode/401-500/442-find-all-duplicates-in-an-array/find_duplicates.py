# LeetCode #442: Find All Duplicates in an Array -- mirror of
# find_duplicates.kara (marking by sign).


def find_duplicates(nums):
    duplicates = []
    for i in range(len(nums)):
        x = abs(nums[i])
        if nums[x - 1] < 0:
            duplicates.append(x)
        else:
            nums[x - 1] = -nums[x - 1]
    return duplicates


def show_list(values):
    return "[" + ",".join(str(v) for v in values) + "]"


# The duplicates in ascending order: the problem allows any order, and
# the arms find them in different ones.
def sorted_duplicates(nums):
    return sorted(find_duplicates(list(nums)))


def show(nums):
    print(f"{show_list(nums)}: {show_list(sorted_duplicates(nums))}")


seed = 442


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n numbers from [1, n]: d of them twice and n - 2d once, shuffled.
def random_case(n, d):
    values = list(range(1, n + 1))
    for i in range(n):
        j = i + next_random() % (n - i)
        values[i], values[j] = values[j], values[i]
    nums = values[: n - d] + values[:d]
    for i in range(n):
        j = i + next_random() % (n - i)
        nums[i], nums[j] = nums[j], nums[i]
    return nums


def main():
    show([4, 3, 2, 7, 8, 2, 3, 1])
    show([1, 1, 2])
    show([1])
    show([2, 2])
    show([3, 1, 2])
    show([1, 1, 2, 2, 3, 3])
    show([6, 5, 4, 3, 2, 1, 6, 5, 4, 3])
    show([5, 4, 3, 2, 1, 5])
    # 300 random arrays of 1 to 200 numbers, from no duplicates to as
    # many as fit.
    found = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 200
        d = next_random() % (n // 2 + 1)
        for x in sorted_duplicates(random_case(n, d)):
            found += 1
            checksum = (checksum * 31 + x) % 1000000007
        checksum = (checksum * 31) % 1000000007
    print(f"300 random arrays: {found} duplicates, checksum {checksum}")


main()
