# LeetCode #1793: Maximum Score of a Good Subarray -- the bench in Python:
# the ★ arm over 200 random lists of 1000 numbers built once, 40000 calls.


def maximum_score(nums, k):
    n = len(nums)
    i = j = k
    low = nums[k]
    best = low
    while i > 0 or j < n - 1:
        left = nums[i - 1] if i > 0 else 0
        right = nums[j + 1] if j < n - 1 else 0
        if left > right:
            i -= 1
            low = min(low, left)
        else:
            j += 1
            low = min(low, right)
        best = max(best, low * (j - i + 1))
    return best


seed = 1793


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[1 + next_random() % 20000 for _ in range(1000)] for _ in range(200)]
    check = 0
    for call in range(40000):
        nums = lists[(check + call) % 200]
        k = check % 1000
        check = (check * 31 + maximum_score(nums, k)) % 1000000007
    print(f"40000 calls over 200 lists of 1000 numbers: checksum {check}")


main()
