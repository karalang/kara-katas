# LeetCode #2789: Largest Element in an Array after Merge Operations --
# the ★ arm in Python (merge.kara): from the right, the number being
# built takes in each one no greater and starts afresh at a greater one.


def max_array_value(nums):
    n = len(nums)
    held = nums[n - 1]
    for i in range(n - 2, -1, -1):
        held = held + nums[i] if nums[i] <= held else nums[i]
    return held


seed = 2789


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(max_array_value([2, 3, 7, 9, 3]))
    print(max_array_value([5, 3, 3]))
    print(max_array_value([2, 2, 3]))
    n = 100000
    print(max_array_value([1000000] * n))
    print(max_array_value([1000000 - i for i in range(n)]))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        nums = [next_random() % 10 + 1 for _ in range(m)]
        a = max_array_value(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small arrays: largest sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        nums = [wide() % 1000000 + 1 for _ in range(n)]
        a = max_array_value(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"20 arrays of 10^5: largest sum to {total}, checksum {check}")


main()
