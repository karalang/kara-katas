# LeetCode 801 -- Minimum Swaps To Make Sequences Increasing: mirrors the
# harness of min_swap.kara with the ★ arm's two states.
seed = 801


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def min_swap(nums1, nums2):
    n = len(nums1)
    keep, swap = 0, 1
    for i in range(1, n):
        same = nums1[i - 1] < nums1[i] and nums2[i - 1] < nums2[i]
        cross = nums1[i - 1] < nums2[i] and nums2[i - 1] < nums1[i]
        next_keep = next_swap = n + 1
        if same:
            next_keep, next_swap = keep, swap + 1
        if cross:
            next_keep = min(next_keep, swap)
            next_swap = min(next_swap, keep + 1)
        keep, swap = next_keep, next_swap
    return min(keep, swap)


def show(nums1, nums2):
    print(f"{nums1}, {nums2} -> {min_swap(nums1, nums2)}")


def main():
    show([1, 3, 5, 4], [1, 2, 3, 7])
    show([0, 3, 5, 8, 9], [2, 1, 4, 6, 9])
    show([1, 2], [3, 4])
    show([3, 2], [1, 4])
    show([0, 4, 4, 5, 9], [0, 1, 6, 8, 10])
    show([0, 11, 2, 13, 4, 15], [10, 1, 12, 3, 14, 5])
    total = check = 0
    for i in range(300):
        n = 2 + next_random() % 40
        gap = 1 + next_random() % 3
        a, b = [], []
        x = next_random() % 5
        y = next_random() % 5
        for _ in range(n):
            x += 1 + next_random() % gap
            y += 1 + next_random() % gap
            if next_random() % 2 == 0:
                a.append(x)
                b.append(y)
            else:
                a.append(y)
                b.append(x)
        k = min_swap(a, b)
        total += k
        check = (check * 131 + k + i) % 1000000007
    print(f"300 random pairs: {total} swaps in all, checksum {check}")


main()
