# Benchmark: LeetCode #1085 Sum of Digits in the Minimum Number -- the ★
# arm. Mirrors sum_of_digits.kara, .rs, .c and go-seq/.


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


seed = 1085


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 5000
    arrays = []
    for _ in range(2000):
        low = next_random() % 100 + 1
        arrays.append([low + next_random() % (101 - low) for _ in range(100)])
    ones = 0
    check = 0
    for r in range(rounds):
        for i in range(2000):
            a = sum_of_digits(arrays[(r * 7 + i) % 2000])
            ones += a
            check = (check * 31 + a + i) % 1000000007
    print(f"{rounds} rounds over 2000 arrays of 100 values: {ones} answer 1, checksum {check}")


main()
