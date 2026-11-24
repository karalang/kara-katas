# LeetCode #2535: Difference Between Element Sum and Digit Sum of an Array
# -- Python mirror of the ★ arm (difference.kara): one pass, each number
# added to the element sum and its digits, taken off by % 10 and // 10, to
# the digit sum; the answer the absolute difference.


def difference_of_sum(nums):
    element_sum = 0
    digit_sum = 0
    for x in nums:
        element_sum += x
        rest = x
        while rest > 0:
            digit_sum += rest % 10
            rest //= 10
    return abs(element_sum - digit_sum)


seed = 2535


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


def main():
    global seed
    # LeetCode's two examples, then six more
    fixed = [
        [1, 15, 6, 3],
        [1, 2, 3, 4],
        [2000],
        [1999],
        [9, 99, 999],
        [10, 100, 1000],
        [1, 1, 1, 1, 1],
        [1234, 567, 89],
    ]
    for nums in fixed:
        print(f"{show(nums)} -> {difference_of_sum(nums)}")
    # 3000 random lists of 1 to 20 numbers from 1 to 2000, and 1000 of 1
    # to 2000: the sum of the answers and a checksum
    seed = 2535
    for count, most in [(3000, 20), (1000, 2000)]:
        total = 0
        check = 0
        for _ in range(count):
            n = next_random() % most + 1
            nums = [next_random() % 2000 + 1 for _ in range(n)]
            a = difference_of_sum(nums)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"{count} random lists of up to {most} numbers: total {total}, checksum {check}")


main()
