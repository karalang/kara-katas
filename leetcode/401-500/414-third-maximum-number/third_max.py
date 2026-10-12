# LeetCode #414: Third Maximum Number -- mirror of third_max.kara
# (three slots).


def third_max(nums):
    first = second = third = None
    for x in nums:
        if x == first or x == second or x == third:
            continue
        if first is None:
            first = x
            continue
        if x > first:
            third = second
            second = first
            first = x
            continue
        if second is None:
            second = x
            continue
        if x > second:
            third = second
            second = x
            continue
        if third is None or x > third:
            third = x
    return third if third is not None else first


seed = 414


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}]: {third_max(nums)}")


show([3, 2, 1])
show([1, 2])
show([2, 2, 3, 1])
show([5])
show([4, 4, 4, 4])
show([1, 2, 2])
show([1, 1, 2, 2, 3, 3])
show([10, 9, 8, 7, 6, 5])
show([-1, -2, -3, -4])
show([-2147483648, 2147483647, 0])
show([-2147483648, -2147483648, 1, 1])
total = 0
checksum = 0
for _ in range(2000):
    n = 1 + step() % 40
    width = 1 + step() % 20
    centre = step() % 2001 - 1000
    nums = [centre + step() % width for _ in range(n)]
    answer = third_max(nums)
    total += answer
    checksum = (checksum * 31 + answer + 2000) % 1000000007
print(f"2000 random arrays: total {total}, checksum {checksum}")
