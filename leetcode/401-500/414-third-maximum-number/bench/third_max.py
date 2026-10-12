# LeetCode #414: Third Maximum Number -- Python mirror of third_max.kara
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


def value():
    high = step()
    low = step()
    return high * 131072 + low * 4 - 2147483648


def main():
    n = 10000
    rounds = 50000
    nums = [value() for _ in range(n)]
    total = 0
    checksum = 0
    for r in range(rounds):
        nums[r * 7919 % n] = value()
        answer = third_max(nums)
        total += answer
        checksum = (checksum * 31 + answer % 1000000007 + 1000000007) % 1000000007
    print(f"{rounds} rounds on {n} numbers: total {total}, checksum {checksum}")


main()
