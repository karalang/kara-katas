# LeetCode #1636: Sort Array by Increasing Frequency -- the Python mirror of
# the ★ arm: each value counted, then sorted by (count, -value).

from collections import Counter


def frequency_sort(nums):
    count = Counter(nums)
    return sorted(nums, key=lambda x: (count[x], -x))


# ---- the harness: the same as every arm's ---------------------------------

seed = 1636


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, spread):
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        nums = [next_random() % (2 * spread + 1) - spread for _ in range(n)]
        for x in frequency_sort(nums):
            check = (check * 31 + x + 1000) % 1000000007
    print(f"{count} arrays of up to {most} values: checksum {check}")


def show(values):
    print("[" + ", ".join(str(x) for x in values) + "]")


show(frequency_sort([1, 1, 2, 2, 2, 3]))
show(frequency_sort([2, 3, 1, 3, 2]))
show(frequency_sort([-1, 1, -6, 4, 5, -6, 1, 4, 1]))
show(frequency_sort([7]))
show(frequency_sort([4, -2, 9, 0]))
show(frequency_sort([5, 5, 5]))
batch(3000, 8, 3)
batch(300, 100, 100)
batch(5, 100000, 100)
