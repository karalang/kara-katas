# LeetCode #523: Continuous Subarray Sum -- mirror of the ★ arm (first
# index of each prefix remainder); see check_subarray_sum.kara.


def check_subarray_sum(nums, k):
    first = {0: -1}
    rem = 0
    for i in range(len(nums)):
        rem = (rem + nums[i]) % k
        if rem in first:
            if i - first[rem] >= 2:
                return True
        else:
            first[rem] = i
    return False


seed = 523


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def b(x):
    return "true" if x else "false"


def show(nums, k):
    print(f"[{', '.join(map(str, nums))}], k = {k}: {b(check_subarray_sum(nums, k))}")


def main():
    show([23, 2, 4, 6, 7], 6)
    show([23, 2, 6, 4, 7], 6)
    show([23, 2, 6, 4, 7], 13)
    show([0, 0], 1)
    show([0], 1)
    show([5, 0, 0, 0], 3)
    show([1, 0], 2)
    show([1, 2, 12], 6)
    show([6], 6)
    show([2, 4], 6)
    show([1000000000, 1000000000], 2147483647)
    yes = 0
    checksum = 0
    for i in range(3000):
        n = 1 + next_random() % 30
        k = 1 + next_random() % 1000
        nums = [next_random() % 1000 for _ in range(n)]
        if check_subarray_sum(nums, k):
            yes += 1
            checksum = (checksum * 31 + i + 1) % 1000000007
    print(f"3000 random arrays: {yes} true, checksum {checksum}")
    big = [1 + next_random() % 20000 for _ in range(100000)]
    middle = sum(big[25000:75000])
    print(f"100000 numbers, k = 2147483647: {b(check_subarray_sum(big, 2147483647))}; k = {middle}: {b(check_subarray_sum(big, middle))}")


main()
