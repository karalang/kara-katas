# LeetCode #704: Binary Search -- a closed range.
#
# A mirror of binary_search.kara (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def show(nums, target):
    print(f"{nums} target {target}: {search(nums, target)}")


def random_sorted(n, low, gap):
    out = []
    v = low
    while len(out) < n and v <= 9999:
        out.append(v)
        v += 1 + next_random() % gap
    return out


def main():
    global seed
    example = [-1, 0, 3, 5, 9, 12]
    for t in [9, 2, -1, 12, -9999, 9999, 4]:
        show(example, t)
    show([5], 5)
    show([5], 4)
    show([5], 6)
    show([-9999, 9999], -9999)
    show([-9999, 9999], 9999)
    show([-9999, 9999], 0)
    big = [-9999 + 2 * i for i in range(10000)]
    found = 0
    total = 0
    for target in range(-9999, 10000):
        at = search(big, target)
        if at >= 0:
            found += 1
        total = (total * 31 + at + 1) % 1000000007
    print(f"10000 values, 19999 targets: {found} found, checksum {total}")
    seed = 704
    found = 0
    total = 0
    for _ in range(1000):
        n = 1 + next_random() % 300
        low = next_random() % 19999 - 9999
        gap = 1 + next_random() % 60
        nums = random_sorted(n, low, gap)
        target = next_random() % 19999 - 9999
        if next_random() % 2 == 0:
            target = nums[next_random() % len(nums)]
        at = search(nums, target)
        if at >= 0:
            found += 1
        total = (total * 31 + at + 1) % 1000000007
    print(f"1000 random arrays: {found} found, checksum {total}")


main()
