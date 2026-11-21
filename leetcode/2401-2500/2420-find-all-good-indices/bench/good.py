# LeetCode #2420: Find All Good Indices -- the bench, the ★ arm: the run of
# values ending at each index without rising, from the left, and the run
# starting at each index without falling, from the right.

seed = 2420


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def good_indices(nums, k):
    n = len(nums)
    falling = [1] * n
    rising = [1] * n
    for i in range(1, n):
        if nums[i] <= nums[i - 1]:
            falling[i] = falling[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if nums[i] <= nums[i + 1]:
            rising[i] = rising[i + 1] + 1
    good = []
    for i in range(k, n - k):
        if falling[i - 1] >= k and rising[i + 1] >= k:
            good.append(i)
    return good


def main():
    arrays = []
    for _ in range(10):
        nums = []
        down = True
        for i in range(100000):
            if i == 0:
                nums.append(1 + (next_random() * 32768 + next_random()) % 1000000)
            else:
                if next_random() % 60 == 0:
                    down = not down
                d = next_random() % 41
                v = nums[i - 1] - d if down else nums[i - 1] + d
                nums.append(min(max(v, 1), 1000000))
        arrays.append(nums)
    check = 0
    for p in range(100):
        for a in range(10):
            good = good_indices(arrays[a], 1 + (p + a) % 40)
            check = (check * 31 + len(good) + sum(good) % 1000003) % 1000000007
    print(f"100 passes over 10 arrays of 10^5 values: checksum {check}")


main()
