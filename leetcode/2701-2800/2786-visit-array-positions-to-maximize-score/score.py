# LeetCode #2786: Visit Array Positions to Maximize Score -- the ★ arm in
# Python (score.kara): the best score of a walk ending on each parity,
# each number extending the better of its own parity's and the other's
# less x.


def max_score(nums, x):
    unreached = -1000000000000000
    best = [unreached, unreached]
    best[nums[0] % 2] = nums[0]
    for v in nums[1:]:
        p = v % 2
        best[p] = max(best[p], best[1 - p] - x) + v
    return max(best[0], best[1])


seed = 2786


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(max_score([2, 3, 6, 1, 9, 2], 5))
    print(max_score([2, 4, 6, 8], 3))
    print(max_score([2, 3, 3, 3], 4))
    print(max_score([2, 9, 9, 9], 4))
    n = 100000
    alternating = [1000000 - i % 2 for i in range(n)]
    print(max_score(alternating, 1))
    print(max_score(alternating, 1000000))
    total = 0
    check = 0
    for _ in range(3000):
        m = next_random() % 11 + 2
        nums = [next_random() % 10 + 1 for _ in range(m)]
        x = next_random() % 10 + 1
        a = max_score(nums, x)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small arrays: scores sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        nums = [wide() % 1000000 + 1 for _ in range(n)]
        x = wide() % 1000000 + 1
        a = max_score(nums, x)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"20 arrays of 10^5: scores sum to {total}, checksum {check}")


main()
