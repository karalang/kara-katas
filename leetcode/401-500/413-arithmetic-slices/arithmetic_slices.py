# LeetCode #413: Arithmetic Slices -- mirror of arithmetic_slices.kara
# (slices ending here).


def number_of_arithmetic_slices(nums):
    ending = 0
    total = 0
    for i in range(2, len(nums)):
        if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:
            ending += 1
            total += ending
        else:
            ending = 0
    return total


seed = 413


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}]: {number_of_arithmetic_slices(nums)}")


show([1, 2, 3, 4])
show([1])
show([1, 2])
show([1, 3, 5])
show([7, 7, 7, 7, 7])
show([3, -1, -5, -9])
show([1, 2, 3, 8, 9, 10])
show([1, 2, 4, 8, 16])
show([1, 2, 3, 5, 7, 9, 11])
show([-1000, 0, 1000, 2000, 2000, 2000])
total = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 60
    nums = [step() % 21 - 10]
    while len(nums) < n:
        diff = step() % 7 - 3
        run = 1 + step() % 8
        for _ in range(run):
            if len(nums) < n:
                nums.append(nums[-1] + diff)
    answer = number_of_arithmetic_slices(nums)
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"2000 random arrays: total {total}, checksum {checksum}")
