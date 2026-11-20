# LeetCode #1752: Check if Array Is Sorted and Rotated -- the bench
# (rotated.kara in Python): count the drops.


def check_rotated(nums):
    drops = sum(1 for a, b in zip(nums, nums[1:]) if a > b)
    wrap = 1 if nums[-1] > nums[0] else 0
    return drops + wrap <= 1


seed = 1752


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds, n = 100000, 5, 100
arrays = []
for _ in range(count):
    nums = [next_random() % 100 + 1 for _ in range(n)]
    if next_random() % 2 == 0:
        nums.sort()
        k = next_random() % n
        nums = nums[k:] + nums[:k]
    arrays.append(nums)
yes = 0
check = 0
for r in range(rounds):
    for nums in arrays:
        answer = check_rotated(nums)
        yes += answer
        check = (check * 31 + (2 if answer else 1) + r) % 1000000007
print(f"{count} arrays of {n} values, {rounds} rounds: {yes} sorted and rotated, checksum {check}")
