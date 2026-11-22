# LeetCode #2762: Continuous Subarrays -- the bench (continuous.kara in
# Python): a window with two deques of indices whose fronts are its least
# and greatest, shrunk from the left while those lie more than 2 apart.
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


def main():
    count, rounds = 20, 10
    cases = []
    for _ in range(count):
        value = 500000000
        nums = []
        for _ in range(100000):
            value += next_random() % 5 - 2
            nums.append(value)
        cases.append(nums)
    total = check = 0
    for r in range(rounds):
        for nums in cases:
            found = continuous_subarrays(nums)
            total += found
            check = (check * 31 + found + r) % 1000000007
    print(f"{count} walks of 100000, {rounds} rounds: subarrays sum to {total}, checksum {check}")


main()
