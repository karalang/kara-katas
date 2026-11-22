# LeetCode #2799: Count Complete Subarrays in an Array -- the ★ arm in
# Python (complete.kara): a window slid along the ends, its start moved
# on while the window stays complete without its first number, and every
# start up to the window's counted.


def count_complete_subarrays(nums):
    d = len(set(nums))
    counts = {}
    start = 0
    complete = 0
    for v in nums:
        counts[v] = counts.get(v, 0) + 1
        while len(counts) == d:
            first = nums[start]
            held = counts[first]
            if held == 1:
                break
            counts[first] = held - 1
            start += 1
        if len(counts) == d:
            complete += start + 1
    return complete


seed = 2799


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(count_complete_subarrays([1, 3, 1, 2, 2]))
    print(count_complete_subarrays([5, 5, 5, 5]))
    n = 1000
    print(count_complete_subarrays([2000 - i for i in range(n)]))
    print(count_complete_subarrays([i % 10 + 1 for i in range(n)]))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 12 + 1
        nums = [next_random() % 4 + 1 for _ in range(m)]
        a = count_complete_subarrays(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small arrays: complete sum to {total}, checksum {check}")
    total = 0
    check = 0
    for c in range(50):
        top = 2000 if c % 2 == 0 else 20
        nums = [wide() % top + 1 for _ in range(n)]
        a = count_complete_subarrays(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"50 arrays of 1000: complete sum to {total}, checksum {check}")


main()
