# LeetCode #1671: Minimum Number of Removals to Make Mountain Array -- the
# Python mirror of the ★ arm: the longest rise into each value and the
# longest fall out of it, O(n^2).


def minimum_mountain_removals(nums):
    n = len(nums)
    up = [1] * n
    down = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                up[i] = max(up[i], up[j] + 1)
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:
                down[i] = max(down[i], down[j] + 1)
    longest = 0
    for i in range(1, n - 1):
        if up[i] > 1 and down[i] > 1:
            longest = max(longest, up[i] + down[i] - 1)
    return n - longest


# ---- the harness: the same as the Kāra arms -------------------------------

seed = 1671


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, most):
    nums = [(next_random() * 32768 + next_random()) % most + 1 for _ in range(n)]
    peak = next_random() % (n - 2) + 1
    nums[peak] = most + 1
    return nums


def batch(count, longest, most):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % (longest - 2) + 3
        nums = random_nums(n, most)
        removed = minimum_mountain_removals(nums)
        total += removed
        check = (check * 31 + removed + n) % 1000000007
    print(f"{count} arrays of up to {longest} values up to {most}: {total} removals, checksum {check}")


print(minimum_mountain_removals([1, 3, 1]))
print(minimum_mountain_removals([2, 1, 1, 5, 6, 2, 3, 1]))
print(minimum_mountain_removals([1, 2, 3, 4, 3, 2, 1]))
print(minimum_mountain_removals([1, 1, 2, 2, 3, 3, 2, 2, 1, 1]))
print(minimum_mountain_removals([9, 8, 1, 7, 6, 5]))
print(minimum_mountain_removals([1, 2, 3, 4, 9, 1]))
batch(3000, 12, 5)
batch(300, 1000, 1000000000)
batch(30, 1000, 10)
