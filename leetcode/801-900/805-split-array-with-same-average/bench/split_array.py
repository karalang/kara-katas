# LeetCode 805 -- Split Array With Same Average: the bench, mirroring
# split_array.kara with the same sums by size.
seed = 805


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def split_array_same_average(nums):
    n = len(nums)
    total = sum(nums)
    half = n // 2
    sums = [set() for _ in range(half + 1)]
    sums[0].add(0)
    for x in nums:
        for k in range(half, 0, -1):
            for s in list(sums[k - 1]):
                sums[k].add(s + x)
    for k in range(1, half + 1):
        if total * k % n == 0 and total * k // n in sums[k]:
            return True
    return False


def main():
    arrays = []
    for a in range(16):
        nums = []
        total = 0
        for _ in range(29):
            x = next_random() % 300
            nums.append(x)
            total += x
        if a % 2 == 0:
            last = next_random() % 300
        else:
            last = (31 - total % 30) % 30 + 30 * (next_random() % 9)
        nums.append(last)
        arrays.append(nums)
    rounds = 400
    yes = 0
    check = 0
    for r in range(rounds):
        can = split_array_same_average(arrays[r % 16])
        if can:
            yes += 1
        check = (check * 131 + (1 if can else 2)) % 1000000007
    print(f"{rounds} rounds of 30 numbers: {yes} can be split, checksum {check}")


main()
