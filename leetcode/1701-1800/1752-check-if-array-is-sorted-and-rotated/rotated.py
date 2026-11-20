# LeetCode #1752: Check if Array Is Sorted and Rotated -- mirrors
# rotated.kara (the ★ arm): count the drops.


def check_rotated(nums):
    drops = sum(1 for a, b in zip(nums, nums[1:]) if a > b)
    wrap = 1 if nums[-1] > nums[0] else 0
    return drops + wrap <= 1


seed = 1752


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(most, top):
    n = next_random() % most + 1
    nums = [next_random() % top + 1 for _ in range(n)]
    if next_random() % 2 == 1:
        return nums
    nums.sort()
    r = next_random() % n
    nums = nums[r:] + nums[:r]
    if next_random() % 2 == 1:
        i = next_random() % n
        nums[i] = next_random() % top + 1
    return nums


def batch(count, most, top):
    yes = 0
    check = 0
    for _ in range(count):
        nums = draw(most, top)
        answer = check_rotated(nums)
        yes += answer
        check = (check * 31 + (2 if answer else 1) + len(nums)) % 1000000007
    print(f"{count} arrays of up to {most} values from 1 to {top}: {yes} sorted and rotated, checksum {check}")


for nums in [[3, 4, 5, 1, 2], [2, 1, 3, 4], [1, 2, 3], [7], [5, 5, 5, 5], [2, 2, 3, 1, 2], [1, 3, 2, 4, 1]]:
    print("true" if check_rotated(nums) else "false")
batch(3000, 6, 3)
batch(3000, 100, 100)
