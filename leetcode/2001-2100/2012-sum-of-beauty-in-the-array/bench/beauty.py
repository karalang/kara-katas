# LeetCode #2012: Sum of Beauty in the Array -- the ★ arm's benchmark, a
# mirror of beauty.kara.


def sum_of_beauties(nums):
    n = len(nums)
    min_after = [0] * n
    min_after[n - 1] = nums[n - 1]
    for i in range(n - 2, -1, -1):
        min_after[i] = min(min_after[i + 1], nums[i])
    max_before = nums[0]
    total = 0
    for i in range(1, n - 1):
        if max_before < nums[i] < min_after[i + 1]:
            total += 2
        elif nums[i - 1] < nums[i] < nums[i + 1]:
            total += 1
        max_before = max(max_before, nums[i])
    return total


seed = 2012


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for a in range(1000):
        rise = a % 11
        nums = []
        for i in range(2000):
            if i > 0 and next_random() % 10 < rise:
                nums.append(min(nums[i - 1] + next_random() % 3 + 1, 100000))
            else:
                nums.append(next_random() % 100000 + 1)
        arrays.append(nums)
    calls = 0
    total = 0
    check = 0
    for _ in range(5):
        for a in range(len(arrays)):
            answer = sum_of_beauties(arrays[a])
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
