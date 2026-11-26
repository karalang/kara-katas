# LeetCode #1493: Longest Subarray of 1's After Deleting One Element -- the
# Python mirror of the ★ arm: a sliding window holding at most one 0.


def longest_subarray(nums):
    best = zeros = left = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > 1:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left)
    return best


seed = 1493


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    f = longest_subarray
    print(f"{f([1, 1, 0, 1])} {f([0, 1, 1, 1, 0, 1, 1, 0, 1])} {f([1, 1, 1])}")
    print(f"{f([1])} {f([0])} {f([0, 0, 0])} {f([0, 1, 1, 0])} {f([1, 1, 0, 0, 1, 1, 1])} {f([1, 0, 1, 1, 0, 1, 1, 1, 1])}")
    ones = [1] * 100000
    middle = ones[:]
    middle[50000] = 0
    mostly = [0 if next_random() % 10 == 0 else 1 for _ in range(100000)]
    print(f"100000 digits: {f(ones)} | {f(middle)} | {f(mostly)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        zeros = 1 + next_random() % 4
        nums = [0 if next_random() % 5 < zeros else 1 for _ in range(n)]
        check = (check * 31 + f(nums) + 1) % 1000000007
    print(f"3000 random arrays: checksum {check}")


main()
