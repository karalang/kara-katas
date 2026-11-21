# LeetCode #2455: Average Value of Even Numbers That Are Divisible by
# Three -- Python mirror of average.kara: one pass sums and counts the
# values divisible by 6, and the average is the sum floor-divided by the
# count, or 0 when there are none.


def average_value(nums):
    total = 0
    count = 0
    for x in nums:
        if x % 6 == 0:
            total += x
            count += 1
    return 0 if count == 0 else total // count


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    print(average_value([1, 3, 6, 10, 12, 15]))
    print(average_value([1, 2, 4, 7, 10]))
    print(average_value([6]))
    print(average_value([2, 4, 8, 3, 9, 15, 1000]))
    print(average_value([6, 12, 13, 18, 30]))
    print(average_value([996] * 1000))
    print(average_value(list(range(1, 1001))))
    seed = 2455
    wide = [1 + next_random() % 1000 for _ in range(1000)]
    print(f"1000 values up to 1000: {average_value(wide)}")
    narrow = [1 + next_random() % 20 for _ in range(1000)]
    print(f"1000 values up to 20: {average_value(narrow)}")
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 8
        nums = [1 + next_random() % 60 for _ in range(n)]
        answer = average_value(nums)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
