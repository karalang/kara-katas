# LeetCode #896 bench: the ★ arm (one pass, two flags) over 16 arrays of
# 100,000 numbers, LeetCode's largest, built once as random walks, half
# rising and half falling. Each of 2,000 rounds sets one random place of
# one array to the number before it, which keeps the array monotonic, or
# in every other round to a random number, asks whether the array is
# monotonic, and puts the number back. The same algorithm as
# is_monotonic.kara.


def is_monotonic(nums):
    rising = True
    falling = True
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            falling = False
        if nums[i] < nums[i - 1]:
            rising = False
    return rising or falling


seed = 896


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for k in range(16):
        nums = []
        x = -100000 if k % 2 == 0 else 100000
        for _ in range(100000):
            nums.append(x)
            step = next_random() % 2
            x = x + step if k % 2 == 0 else x - step
        arrays.append(nums)
    monotonic = 0
    check = 0
    for _ in range(2000):
        a = next_random() % 16
        p = next_random() * 32768
        p = (p + next_random()) % 100000
        random = next_random() * 32768
        random = (random + next_random()) % 200001 - 100000
        old = arrays[a][p]
        value = arrays[a][p - 1] if next_random() % 2 == 0 and p > 0 else random
        arrays[a][p] = value
        got = is_monotonic(arrays[a])
        arrays[a][p] = old
        if got:
            monotonic += 1
        check = (check * 131 + p * 2 + (1 if got else 0)) % 1000000007
    print(f"2000 rounds over 16 arrays of 100000 numbers: {monotonic} monotonic, checksum {check}")


main()
