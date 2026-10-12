# LeetCode #416: Partition Equal Subset Sum -- Python mirror of
# can_partition.kara (sums up to half).


def can_partition(nums):
    total = 0
    for x in nums:
        total += x
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


def main():
    n = 200
    rounds = 2000
    nums = []
    total = 0
    for _ in range(n):
        x = 1 + step() % 100
        nums.append(x)
        total += x
    if total % 2 != 0:
        nums[0] += 1 if nums[0] < 100 else -1
    yes = 0
    checksum = 0
    for r in range(rounds):
        i = step() % n
        j = step() % n
        if nums[i] < 100 and nums[j] > 1:
            nums[i] += 1
            nums[j] -= 1
        answer = can_partition(nums)
        if answer:
            yes += 1
        checksum = (checksum * 31 + nums[i] + (r if answer else 0)) % 1000000007
    print(f"{rounds} rounds on {n} numbers: {yes} can be split, checksum {checksum}")


main()
