# LeetCode #2366: Minimum Replacements to Sort the Array -- the Python
# mirror of the ★ arm: greedy from the right, a value over the bound
# split into the fewest pieces that fit, the bound becoming the smallest
# piece of the most even split.


def minimum_replacement(nums):
    n = len(nums)
    bound = nums[n - 1]
    ops = 0
    for i in range(n - 2, -1, -1):
        v = nums[i]
        if v <= bound:
            bound = v
        else:
            k = (v + bound - 1) // bound
            ops += k - 1
            bound = v // k
    return ops


SEED = [2366]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; one value; 10^5 values of 10^9 before a 1;
    # 10^5 values falling from 10^9; 10^5 values rising; then 2000 random
    # arrays of 1 to 40 values from 1 to 1 to 60
    print(minimum_replacement([3, 9, 3]))
    print(minimum_replacement([1, 2, 3, 4, 5]))
    print(minimum_replacement([7]))
    print(minimum_replacement([1000000000] * 99999 + [1]))
    print(minimum_replacement([1000000000 - i * 9999 for i in range(100000)]))
    print(minimum_replacement([i + 1 for i in range(100000)]))
    check = 0
    already = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        top = 1 + next_random() % 60
        nums = [1 + next_random() % top for _ in range(n)]
        ops = minimum_replacement(nums)
        check = (check * 31 + ops) % 1000000007
        if ops == 0:
            already += 1
    print(f"2000 arrays: checksum {check}, {already} already sorted")


if __name__ == "__main__":
    main()
