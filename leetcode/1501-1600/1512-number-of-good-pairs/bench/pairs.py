# LeetCode #1512: Number of Good Pairs -- the bench: 50 arrays of 200000
# numbers from 1 to 100 built once, then each counted four times by the
# ★ arm.


def num_identical_pairs(nums):
    seen = [0] * 101
    pairs = 0
    for x in nums:
        pairs += seen[x]
        seen[x] += 1
    return pairs


seed = 1512


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


arrays = [[next_random() % 100 + 1 for _ in range(200000)] for _ in range(50)]
check = 0
for _ in range(4):
    for nums in arrays:
        check = (check * 31 + num_identical_pairs(nums) + 1) % 1000000007
print(f"200 counts over 50 arrays of 200000 numbers: checksum {check}")
