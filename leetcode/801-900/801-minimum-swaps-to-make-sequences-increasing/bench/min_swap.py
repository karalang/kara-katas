# LeetCode 801 -- Minimum Swaps To Make Sequences Increasing: the bench,
# in Python. Mirrors min_swap.kara: two states, left alone and swapped.
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


def main():
    n = 100000
    pairs = []
    for _ in range(16):
        a, b = [], []
        x = y = 0
        for _ in range(n):
            x += 1 + next_random() % 2
            y += 1 + next_random() % 2
            if next_random() % 2 == 0:
                a.append(x)
                b.append(y)
            else:
                a.append(y)
                b.append(x)
        pairs.append((a, b))
    rounds = 2000
    total = check = 0
    for r in range(rounds):
        a, b = pairs[r % 16]
        k = min_swap(a, b)
        total += k
        check = (check * 131 + k) % 1000000007
    print(f"{rounds} rounds of {n} places: {total} swaps in all, checksum {check}")


main()
