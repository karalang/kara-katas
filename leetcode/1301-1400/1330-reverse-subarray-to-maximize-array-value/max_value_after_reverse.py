# LeetCode #1330: Reverse Subarray To Maximize Array Value -- Python mirror
# of the ★ arm and its harness.


def max_value_after_reverse(nums):
    n = len(nums)
    total = 0
    gain = 0
    high_low = -(2**31)
    low_high = 2**31 - 1
    for i in range(n - 1):
        a, b = nums[i], nums[i + 1]
        d = abs(a - b)
        total += d
        gain = max(gain, abs(nums[0] - b) - d)
        gain = max(gain, abs(nums[n - 1] - a) - d)
        high_low = max(high_low, min(a, b))
        low_high = min(low_high, max(a, b))
    if n > 1:
        gain = max(gain, 2 * (high_low - low_high))
    return total + gain


seed = 1330


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    swing = [100000 if i % 2 == 0 else -100000 for i in range(400)]
    climb = [i * 495 - 99000 for i in range(400)]
    f = max_value_after_reverse
    print(f"{f([2, 3, 1, 5, 4])} {f([2, 4, 9, 24, 2, 1, 10])} {f([5])} {f([1, 9])} {f([7, 7, 7, 7])} {f([1, 2, 3, 10])} {f(swing)} {f(climb)}")
    check = 0
    total = 0
    for t in range(600):
        n = 1 + next_random() % 400 if t % 20 == 0 else 1 + next_random() % 12
        reach = 10 if t % 3 == 0 else 1000 if t % 3 == 1 else 100000
        nums = [next_random() % (2 * reach + 1) - reach for _ in range(n)]
        got = f(nums)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"600 random arrays: values total {total}, checksum {check}")


main()
