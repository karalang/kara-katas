# LeetCode #2369: Check if There is a Valid Partition For The Array -- the
# bench, the ★ arm in Python: good[i] says whether the first i values
# split into valid blocks, from the last block before i and the values
# before it.


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


def main():
    # array a: about 10^5 values in random blocks of two or three equal
    # values or three rising, the values up to 4^(a + 1); when a is odd, one
    # value near the end then raised by one
    arrays = []
    top = 4
    for a in range(10):
        nums = []
        while len(nums) < 100000:
            kind = next_random() % 3
            hi = next_random()
            v = 1 + (hi * 32768 + next_random()) % top
            if kind == 0:
                nums += [v, v]
            elif kind == 1:
                nums += [v, v, v]
            else:
                nums += [v, v + 1, v + 2]
        if a % 2 == 1:
            at = len(nums) - 1 - next_random() % 100
            nums[at] += 1
        arrays.append(nums)
        top *= 4
    check = 0
    for p in range(20):
        for a in range(10):
            valid = a + 1 if valid_partition(arrays[a]) else 0
            check = (check * 31 + valid + p) % 1000000007
    print(f"20 passes over 10 arrays of about 10^5 values: checksum {check}")


main()
