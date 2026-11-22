# LeetCode #2817: Minimum Absolute Difference Between Elements With
# Constraint -- the Python mirror of the ★ arm: the numbers at least x
# behind kept sorted (here a list kept in order with bisect, the set's
# stand-in), each number checked against its neighbours there.
import bisect


def min_absolute_difference(nums, x):
    behind = []
    best = 1 << 62
    for i in range(x, len(nums)):
        bisect.insort(behind, nums[i - x])
        v = nums[i]
        k = bisect.bisect_left(behind, v)
        if k < len(behind):
            best = min(best, behind[k] - v)
        if k > 0:
            best = min(best, v - behind[k - 1])
        if best == 0:
            break
    return best


seed = 2817


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(min_absolute_difference([4, 3, 2, 4], 2))
    print(min_absolute_difference([5, 3, 2, 10, 15], 1))
    print(min_absolute_difference([1, 2, 3, 4], 3))
    print(min_absolute_difference([8, 1], 0))
    print(min_absolute_difference([i * 7 + 1 for i in range(2000)], 1000))
    print(min_absolute_difference([2000000 - i * 1000 for i in range(2000)], 1999))
    check = 0
    for _ in range(3000):
        n = next_random() % 10 + 1
        nums = [next_random() % 20 + 1 for _ in range(n)]
        x = next_random() % n
        check = (check * 31 + min_absolute_difference(nums, x)) % 1000000007
    print(f"3000 small arrays: checksum {check}")
    check = 0
    for _ in range(50):
        n = next_random() % 1000 + 1
        nums = [wide() % 1000000000 + 1 for _ in range(n)]
        x = next_random() % n
        check = (check * 31 + min_absolute_difference(nums, x)) % 1000000007
    print(f"50 large arrays: checksum {check}")


main()
