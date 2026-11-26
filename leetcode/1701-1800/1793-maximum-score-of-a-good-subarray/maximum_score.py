# LeetCode #1793: Maximum Score of a Good Subarray -- the ★ arm in Python:
# two pointers out from k, the window grown toward the larger neighbour.


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
    print(f"{maximum_score([1, 4, 3, 7, 4, 5], 3)} {maximum_score([5, 5, 4, 5, 4, 1, 1, 1], 0)}")
    rising = [1, 2, 3, 4, 5]
    print(f"{maximum_score([7], 0)} {maximum_score(rising, 0)} {maximum_score(rising, 4)} {maximum_score([3, 3, 3, 3], 2)} {maximum_score([5, 5, 1, 5, 5], 2)} {maximum_score([1, 2, 3, 2, 1], 2)}")
    full = [20000] * 100000
    saw = [1 + i % 20000 for i in range(100000)]
    wide = [1 + next_random() % 20000 for _ in range(100000)]
    k = next_random() % 100000
    print(f"the most: {maximum_score(full, 0)} {maximum_score(saw, 99999)} {maximum_score(wide, k)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 50
        nums = [1 + next_random() % top for _ in range(n)]
        k = next_random() % n
        check = (check * 31 + maximum_score(nums, k)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
