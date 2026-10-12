# LeetCode #416: Partition Equal Subset Sum -- mirror of can_partition.kara
# (sums up to half).


def can_partition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False
    half = total // 2
    reach = [False] * (half + 1)
    reach[0] = True
    for x in nums:
        s = half
        while s >= x:
            if reach[s - x]:
                reach[s] = True
            s -= 1
    return reach[half]


seed = 416


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    answer = "true" if can_partition(nums) else "false"
    print(f"[{', '.join(str(x) for x in nums)}]: {answer}")


show([1, 5, 11, 5])
show([1, 2, 3, 5])
show([1])
show([7, 7])
show([1, 2])
show([2, 2, 3, 5])
show([3, 3, 3, 4, 5])
show([100, 100, 100, 100, 99, 1])
show([1] * 25 + [100])
big = [100 - i % 2 for i in range(200)]
print(f"200 numbers, 100 and 99 in turn: {'true' if can_partition(big) else 'false'}")
yes = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 40
    limit = 1 + step() % 100
    nums = [1 + step() % limit for _ in range(n)]
    answer = can_partition(nums)
    if answer:
        yes += 1
    checksum = (checksum * 31 + n + (1000 if answer else 0)) % 1000000007
print(f"2000 random arrays: {yes} can be split, checksum {checksum}")
