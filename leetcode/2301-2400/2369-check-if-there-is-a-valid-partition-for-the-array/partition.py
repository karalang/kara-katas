# LeetCode #2369: Check if There is a Valid Partition For The Array -- the
# Python mirror of the ★ arm: good[i] says whether the first i values
# split into valid blocks.


def valid_partition(nums):
    n = len(nums)
    good = [False] * (n + 1)
    good[0] = True
    for i in range(2, n + 1):
        a = nums[i - 1]
        b = nums[i - 2]
        if a == b and good[i - 2]:
            good[i] = True
        if i >= 3 and good[i - 3]:
            c = nums[i - 3]
            if (a == b and b == c) or (b == c + 1 and a == b + 1):
                good[i] = True
    return good[n]


SEED = [2369]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def text(b):
    return "true" if b else "false"


def main():
    # LeetCode's two examples; two values; 10^5 equal values; 99999 and
    # 10^5 values rising by one; 99999 values in rising threes from 10^6
    # down; then 3000 arrays of 2 to 30 values built from random blocks,
    # each block of two or three equal values or three rising, and with a
    # chance of 1 in 3 one value then changed by one
    print(text(valid_partition([4, 4, 4, 5, 6])))
    print(text(valid_partition([1, 1, 1, 2])))
    print(text(valid_partition([7, 7])))
    print(text(valid_partition([1000000] * 100000)))
    rising = list(range(1, 100001))
    print(f"{text(valid_partition(rising[0:99999]))} {text(valid_partition(rising))}")
    threes = [1000000 - 3 * (i // 3) - 2 + i % 3 for i in range(99999)]
    print(text(valid_partition(threes)))
    check = 0
    valid = 0
    for c in range(3000):
        target = 2 + next_random() % 29
        nums = []
        while len(nums) < target:
            kind = next_random() % 3
            v = 1 + next_random() % 6
            if kind == 0:
                nums += [v, v]
            elif kind == 1:
                nums += [v, v, v]
            else:
                nums += [v, v + 1, v + 2]
        if next_random() % 3 == 0:
            at = next_random() % len(nums)
            nums[at] += 1
        if valid_partition(nums):
            valid += 1
            check = (check * 31 + c + len(nums)) % 1000000007
    print(f"3000 arrays: checksum {check}, {valid} valid")


main()
