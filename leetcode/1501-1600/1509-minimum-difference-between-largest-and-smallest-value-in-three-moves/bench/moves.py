# LeetCode #1509: Minimum Difference Between Largest and Smallest Value in
# Three Moves -- the bench: 20 arrays of 100000 numbers built once, then
# each answered five times by the ★ arm.


def min_difference(nums):
    n = len(nums)
    if n <= 4:
        return 0
    s = sorted(nums)
    best = s[n - 1] - s[0]
    for low in range(4):
        best = min(best, s[n - 4 + low] - s[low])
    return best


seed = 1509


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


arrays = []
for _ in range(20):
    nums = []
    for _ in range(100000):
        wide = next_random() * 32768
        wide += next_random()
        nums.append(wide % 2000000001 - 1000000000)
    arrays.append(nums)
check = 0
for _ in range(5):
    for nums in arrays:
        check = (check * 31 + min_difference(nums) % 1000000007 + 1) % 1000000007
print(f"100 answers over 20 arrays of 100000 numbers: checksum {check}")
