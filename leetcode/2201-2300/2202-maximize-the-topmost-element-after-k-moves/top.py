# LeetCode #2202: Maximize the Topmost Element After K Moves -- Python
# mirror of top.kara (the ★ arm).


def maximum_top(nums, k):
    n = len(nums)
    if n == 1:
        return -1 if k % 2 == 1 else nums[0]
    best = -1
    for i in range(min(k - 1, n)):
        best = max(best, nums[i])
    if k < n:
        best = max(best, nums[k])
    return best


seed = 2202


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def show(nums, k):
    print(f"[{', '.join(map(str, nums))}], k {k} -> {maximum_top(nums, k)}")


def main():
    show([5, 2, 2, 4, 0, 6], 4)
    show([2], 1)
    show([7], 2)
    show([1, 9], 1)
    show([3, 1, 8], 3)
    show([4, 6, 1, 9], 0)
    show([2, 5], 1000000000)
    empty = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        nums = [next_random() % 21 for _ in range(n)]
        k = next_random() % 16
        top = maximum_top(nums, k)
        if top < 0:
            empty += 1
        check = (check * 31 + top + 1) % 1000000007
    print(f"3000 piles: {empty} empty, checksum {check}")
    nums = [wide_random() % 1000000001 for _ in range(100000)]
    for k in [0, 1, 50000, 99999, 100000, 100001, 1000000000]:
        print(f"n 100000, k {k} -> {maximum_top(nums, k)}")


main()
