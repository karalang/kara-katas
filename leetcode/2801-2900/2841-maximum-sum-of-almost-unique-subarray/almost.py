# LeetCode #2841: Maximum Sum of Almost Unique Subarray -- the Python
# mirror of the ★ arm: a window of k slid along the array, its sum kept
# and a dict from each value in it to its count.


def max_sum(nums, m, k):
    count = {}
    total = 0
    best = 0
    for i, x in enumerate(nums):
        count[x] = count.get(x, 0) + 1
        total += x
        if i >= k:
            out = nums[i - k]
            total -= out
            left = count[out] - 1
            if left == 0:
                del count[out]
            else:
                count[out] = left
        if i + 1 >= k and len(count) >= m:
            best = max(best, total)
    return best


# ---- the harness: the same in every arm --------------------------------

seed = 2841


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{max_sum([2, 6, 7, 3, 1, 7], 3, 4)} {max_sum([5, 9, 9, 2, 4, 5, 4], 1, 3)} {max_sum([1, 2, 1, 2, 1, 2, 1], 3, 3)}")
    print(f"{max_sum([7], 1, 1)}")
    big = [1000000000 - i for i in range(20000)]
    print(f"{max_sum(big, 20000, 20000)} {max_sum(big, 21, 20)}")
    check = 0
    zero = 0
    for c in range(3050):
        short = c < 3000
        n = next_random() % 8 + 1 if short else next_random() % 2000 + 1
        top = 4 if short else (1000000000 if c % 2 == 0 else 50)
        nums = []
        for _ in range(n):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % top + 1)
        k = next_random() % min(n, 8 if short else 100) + 1
        m = next_random() % k + 1
        best = max_sum(nums, m, k)
        if best == 0:
            zero += 1
        check = (check * 31 + best) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: {zero} with none, checksum {check}")
            check = 0
            zero = 0
    print(f"50 long arrays: {zero} with none, checksum {check}")


main()
