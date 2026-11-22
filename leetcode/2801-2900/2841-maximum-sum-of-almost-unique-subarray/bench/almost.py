# LeetCode #2841: Maximum Sum of Almost Unique Subarray -- the bench,
# mirrored from almost.kara: a window of k slid along the array, its
# sum kept and a dict from each value in it to its count.

seed = 2841


def max_sum(nums, m, k):
    count = {}
    total = 0
    best = 0
    for i in range(len(nums)):
        x = nums[i]
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


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n, rounds = 100, 20000, 20
    cases = []
    for _ in range(count):
        nums = [next_random() % 10000 + 1 for _ in range(n)]
        k = next_random() % 5000 + 1
        m = next_random() % k + 1
        cases.append((nums, m, k))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, m, k in cases:
            best = max_sum(nums, m, k)
            total += best
            check = (check * 31 + best + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: sums total {total}, checksum {check}")


main()
