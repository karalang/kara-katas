# LeetCode #1608: Special Array With X Elements Greater Than or Equal X --
# the Python mirror of special.kara: the numbers sorted largest first,
# `x` special when the `x`th largest is at least `x` and the next is below.


def special_array(nums):
    nums = sorted(nums, reverse=True)
    n = len(nums)
    for x in range(1, n + 1):
        if nums[x - 1] >= x and (x == n or nums[x] < x):
            return x
    return -1


seed = 1608


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = numbers = special = 0
    for _ in range(count):
        a = next_random()
        n = (a * 32768 + next_random()) % most + 1
        nums = []
        for _ in range(n):
            a = next_random()
            nums.append((a * 32768 + next_random()) % (top + 1))
        x = special_array(nums)
        if x >= 0:
            special += 1
        check = mix(check, x)
        numbers += n
    print(f"{count} problems of up to {most} numbers from 0 to {top}: {numbers} numbers, {special} special, checksum {check}")


for nums in [[3, 5], [0, 0], [0, 4, 3, 0, 4], [3, 6, 7, 7, 0], [1], [2, 2], [1000, 1000, 1000]]:
    print(special_array(nums))
batch(3000, 5, 6)
batch(3000, 100, 1000)
batch(30, 100000, 100000)
