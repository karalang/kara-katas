# Benchmark for #446: mirror of arithmetic_slices.kara (a map of
# differences per index) on 20 random arrays of 1,000 values from -500
# to 499, built once.


def number_of_arithmetic_slices(nums):
    n = len(nums)
    ending = []
    total = 0
    for i in range(n):
        here = {}
        for j in range(i):
            d = nums[i] - nums[j]
            before = ending[j].get(d, 0)
            total += before
            here[d] = here.get(d, 0) + before + 1
        ending.append(here)
    return total


seed = 446


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 20
    n = 1000
    arrays = []
    for _ in range(count):
        arrays.append([next_random() % 1000 - 500 for _ in range(n)])
    total = 0
    checksum = 0
    for nums in arrays:
        answer = number_of_arithmetic_slices(nums)
        total += answer
        checksum = (checksum * 31 + answer % 1000000007) % 1000000007
    print(f"{count} arrays of {n}: {total} slices, checksum {checksum}")


main()
