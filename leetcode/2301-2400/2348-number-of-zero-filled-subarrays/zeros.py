# LeetCode #2348: Number of Zero-Filled Subarrays -- the Python mirror of
# the ★ arm: the length of the run of zeros ending at each place, summed,
# since that many zero-filled subarrays end there.


def zero_filled_subarray(nums):
    run = 0
    total = 0
    for x in nums:
        if x == 0:
            run += 1
        else:
            run = 0
        total += run
    return total


SEED = [2348]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's three examples; then one zero, 10^5 zeros, zeros between
    # every other value, and 10^5 values with every third one not zero
    print(zero_filled_subarray([1, 3, 0, 0, 2, 0, 0, 4]))
    print(zero_filled_subarray([0, 0, 0, 2, 0, 0]))
    print(zero_filled_subarray([2, 10, 2019]))
    print(zero_filled_subarray([0]))
    print(zero_filled_subarray([0] * 100000))
    print(zero_filled_subarray([i % 2 * 1000000000 for i in range(100000)]))
    print(zero_filled_subarray([-1 if i % 3 == 2 else 0 for i in range(100000)]))
    # 2000 random arrays of 1 to 40 values, each zero with a chance of 1 in
    # 2 to 1 in 5, and otherwise from -10^9 to 10^9 but not 0
    check = 0
    total = 0
    none = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        odds = 2 + next_random() % 4
        nums = []
        for _ in range(n):
            if next_random() % odds == 0:
                nums.append(0)
            else:
                v = (next_random() * 32768 + next_random()) % 1000000000 + 1
                nums.append(v if next_random() % 2 == 0 else -v)
        answer = zero_filled_subarray(nums)
        check = (check * 31 + answer + 1) % 1000000007
        total += answer
        if answer == 0:
            none += 1
    print(f"2000 arrays: checksum {check}, sum {total}, none {none}")


main()
