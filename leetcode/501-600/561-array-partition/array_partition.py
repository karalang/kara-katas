# LeetCode #561: Array Partition -- Python mirror of the ★ arm (sort,
# then every other number); see array_partition.kara.


def array_pair_sum(nums):
    nums = sorted(nums)
    return sum(nums[i] for i in range(0, len(nums), 2))


# ---- test harness ---------------------------------------------------------

seed = 561


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


def show(nums):
    print(f"{fmt(nums)}: {array_pair_sum(nums)}")


def main():
    show([1, 4, 3, 2])
    show([6, 2, 6, 5, 1, 2])
    show([5, -5])
    show([7, 7])
    show([-10000, 10000, -10000, 10000])
    show([8, 7, 6, 5, 4, 3, 2, 1])
    show([-1, -2, -3, -4])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 2 * (1 + step() % 20)
        nums = [step() % 201 - 100 for _ in range(n)]
        s = array_pair_sum(nums)
        total += s
        checksum = (checksum * 31 + s + 1000000) % 1000000007
    print(f"300 random arrays: total {total}, checksum {checksum}")
    print(f"20000 of 10000: {array_pair_sum([10000] * 20000)}")
    print(f"20000 falling: {array_pair_sum([10000 - i for i in range(20000)])}")
    rnd = [step() % 20001 - 10000 for _ in range(20000)]
    print(f"20000 random: {array_pair_sum(rnd)}")


main()
