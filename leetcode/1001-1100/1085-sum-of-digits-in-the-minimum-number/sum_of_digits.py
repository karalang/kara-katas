# LeetCode #1085: Sum of Digits in the Minimum Number -- mirrors
# sum_of_digits.kara (the ★ arm: the least value, its digits summed) and
# its harness; the output is byte-identical.


def sum_of_digits(nums):
    least = nums[0]
    for v in nums:
        if v < least:
            least = v
    s = 0
    while least > 0:
        s += least % 10
        least //= 10
    return 1 if s % 2 == 0 else 0


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    cases = [
        [34, 23, 1, 24, 75, 33, 54, 8],
        [99, 77, 33, 66, 55],
        [1],
        [100],
        [10, 100],
        [19, 28, 37],
        [100, 99, 98, 11],
        [56, 65, 47],
    ]
    for nums in cases:
        print(f"[{', '.join(map(str, nums))}] -> {sum_of_digits(nums)}")
    even = sum(sum_of_digits([v]) for v in range(1, 101))
    print(f"1 to 100 alone: {even} answer 1")
    seed = 1085
    ones = 0
    h = 0
    for i in range(1000):
        n = next_random() % 100 + 1
        nums = [next_random() % 100 + 1 for _ in range(n)]
        a = sum_of_digits(nums)
        ones += a
        h = (h * 31 + a + i) % 1000000007
    print(f"1000 random arrays: {ones} answer 1, checksum {h}")


main()
