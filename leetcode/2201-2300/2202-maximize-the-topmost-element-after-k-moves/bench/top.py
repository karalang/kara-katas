# benchmark's Python mirror of top.kara (LeetCode #2202, the ★ arm): the
# first k - 1 numbers and the one at index k.


def maximum_top(nums, k):
    n = len(nums)
    if n == 1:
        return -1 if k % 2 == 1 else nums[0]
    best = -1
    for i in range(min(k - 1, n)):
        if nums[i] > best:
            best = nums[i]
    if k < n and nums[k] > best:
        best = nums[k]
    return best


seed = 2202


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def main():
    piles = []
    ks = []
    for _ in range(10):
        piles.append([wide_random() % 1000000001 for _ in range(100000)])
        ks.append([wide_random() % 100002 for _ in range(10)])
    check = 0
    for _ in range(50):
        for p in range(10):
            for k in ks[p]:
                check = (check * 31 + maximum_top(piles[p], k) + 1) % 1000000007
    print(f"50 passes over 10 piles: checksum {check}")


main()
