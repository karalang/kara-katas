# LeetCode #2762: Continuous Subarrays -- the ★ arm in Python
# (continuous.kara): a window [left, right] with two deques of indices,
# the values rising in one and falling in the other, so their fronts are
# the window's least and greatest; the window shrinks from the left while
# those two lie more than 2 apart, and each right end adds the window's
# length.
from collections import deque


def continuous_subarrays(nums):
    lows = deque()
    highs = deque()
    left = 0
    count = 0
    for right, v in enumerate(nums):
        while lows and nums[lows[-1]] > v:
            lows.pop()
        while highs and nums[highs[-1]] < v:
            highs.pop()
        lows.append(right)
        highs.append(right)
        while nums[highs[0]] - nums[lows[0]] > 2:
            left += 1
            if lows[0] < left:
                lows.popleft()
            if highs[0] < left:
                highs.popleft()
        count += right - left + 1
    return count


seed = 2762


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def walk(n):
    value = 500000000
    nums = []
    for _ in range(n):
        value += next_random() % 3 - 1
        nums.append(value)
    return nums


def main():
    print(continuous_subarrays([5, 4, 2, 4]))
    print(continuous_subarrays([1, 2, 3]))
    print(continuous_subarrays([7]))
    print(continuous_subarrays([1, 4, 1, 4]))
    print(continuous_subarrays([1000000000] * 100000))
    print(continuous_subarrays(list(range(1, 100001))))
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 30 + 1
        nums = [next_random() % 6 + 1 for _ in range(n)]
        a = continuous_subarrays(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 small arrays: subarrays sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20):
        a = continuous_subarrays(walk(100000))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"20 walks of 100000: subarrays sum to {total}, checksum {check}")


main()
