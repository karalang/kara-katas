# LeetCode #446: Arithmetic Slices II - Subsequence -- mirror of
# arithmetic_slices.kara (a map of differences per index).


def number_of_arithmetic_slices(nums):
    n = len(nums)
    ending = []
    total = 0
    for i in range(n):
        here = {}
        for j in range(i):
            d = nums[i] - nums[j]
            before = ending[j].get(d, 0)
            total += before
            here[d] = here.get(d, 0) + before + 1
        ending.append(here)
    return total


def show(nums):
    print(f"[{','.join(str(x) for x in nums)}]: {number_of_arithmetic_slices(nums)}")


seed = 446


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


show([2, 4, 6, 8, 10])
show([7, 7, 7, 7, 7])
show([1])
show([1, 2])
show([1, 2, 3])
show([0, 2000000000, -294967296])
show([-2147483648, 0, 2147483647, -2147483648, -1, 2147483646])
show([3, -1, -5, -9, 1, 5, 9])
count = 300
total = 0
checksum = 0
for _ in range(count):
    n = 1 + next_random() % 60
    spread = [3, 10, 100, 1000000][next_random() % 4]
    nums = []
    for _ in range(n):
        nums.append(next_random() % spread - spread // 2)
    answer = number_of_arithmetic_slices(nums)
    total += answer
    checksum = (checksum * 31 + answer % 1000000007) % 1000000007
print(f"{count} random arrays: {total} slices, checksum {checksum}")
