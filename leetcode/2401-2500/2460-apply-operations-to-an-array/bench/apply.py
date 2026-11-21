# LeetCode #2460: Apply Operations to an Array -- the bench, the ★ arm in
# Python: the operations in place, then the nonzero values moved forward
# by a write index and the rest filled with zeros.


def apply_operations(nums):
    n = len(nums)
    for i in range(n - 1):
        if nums[i] == nums[i + 1]:
            nums[i] *= 2
            nums[i + 1] = 0
    k = 0
    for i in range(n):
        if nums[i] != 0:
            nums[k] = nums[i]
            k += 1
    for i in range(k, n):
        nums[i] = 0
    return nums


seed = 2460


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 1000 arrays of 2000 values from 0 to 3 built once; then 24 passes,
    # each setting one value of every array from the checksum so far,
    # then answering every array on a copy and folding every value of
    # the answer, plus the pass, into the checksum
    arrays = [[next_random() % 4 for _ in range(2000)] for _ in range(1000)]
    check = 0
    for p in range(24):
        for a in range(len(arrays)):
            arrays[a][(check + a) % 2000] = check % 4
            for v in apply_operations(list(arrays[a])):
                check = (check * 31 + v + p) % 1000000007
    print(f"24 passes over 1000 arrays of 2000: checksum {check}")


main()
