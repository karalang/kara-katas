# LeetCode #448: Find All Numbers Disappeared in an Array -- mirror of
# find_disappeared.kara (marking by sign).


def find_disappeared_numbers(nums):
    for i in range(len(nums)):
        x = abs(nums[i])
        if nums[x - 1] > 0:
            nums[x - 1] = -nums[x - 1]
    return [i + 1 for i in range(len(nums)) if nums[i] > 0]


def lst(values):
    return "[" + ",".join(str(x) for x in values) + "]"


def show(nums):
    print(f"{lst(nums)}: {lst(find_disappeared_numbers(list(nums)))}")


seed = 448


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_case(n):
    if next_random() % 2 == 0:
        return [1 + next_random() % n for _ in range(n)]
    nums = list(range(1, n + 1))
    for i in range(n):
        j = i + next_random() % (n - i)
        nums[i], nums[j] = nums[j], nums[i]
    for _ in range(next_random() % (n // 4 + 1)):
        to = next_random() % n
        nums[to] = nums[next_random() % n]
    return nums


show([4, 3, 2, 7, 8, 2, 3, 1])
show([1, 1])
show([1])
show([2, 2])
show([3, 1, 2])
show([5, 5, 5, 5, 5])
show([2, 3, 4, 5, 6, 6])
show([1, 1, 1, 6, 6, 6])
found = 0
checksum = 0
for _ in range(300):
    n = 1 + next_random() % 200
    for x in find_disappeared_numbers(random_case(n)):
        found += 1
        checksum = (checksum * 31 + x) % 1000000007
    checksum = (checksum * 31) % 1000000007
print(f"300 random arrays: {found} missing, checksum {checksum}")
