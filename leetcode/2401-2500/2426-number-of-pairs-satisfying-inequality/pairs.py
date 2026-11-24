# LeetCode #2426: Number of Pairs Satisfying Inequality -- the Python
# mirror of the ★ arm: with `a[i] = nums1[i] - nums2[i]`, a merge sort
# counting the pairs `i < j` with `a[i] <= a[j] + diff`.

import sys

sys.setrecursionlimit(10000)

seed = 2426


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count_pairs(a, lo, hi, diff):
    if hi - lo < 2:
        return 0
    mid = (lo + hi) // 2
    count = count_pairs(a, lo, mid, diff) + count_pairs(a, mid, hi, diff)
    p = lo
    for j in range(mid, hi):
        while p < mid and a[p] <= a[j] + diff:
            p += 1
        count += p - lo
    merged = []
    i, j = lo, mid
    while i < mid or j < hi:
        if j == hi or (i < mid and a[i] <= a[j]):
            merged.append(a[i])
            i += 1
        else:
            merged.append(a[j])
            j += 1
    a[lo:hi] = merged
    return count


def number_of_pairs(nums1, nums2, diff):
    a = [x - y for x, y in zip(nums1, nums2)]
    return count_pairs(a, 0, len(a), diff)


def random_nums(n, top):
    return [next_random() % (2 * top + 1) - top for _ in range(n)]


def main():
    print(number_of_pairs([3, 2, 5], [2, 2, 1], 1))
    print(number_of_pairs([3, -1], [-2, 2], -1))
    print(number_of_pairs([4, 4, 4, 4, 4], [1, 1, 1, 1, 1], 0))
    print(number_of_pairs([5, 4, 3, 2, 1], [0, 0, 0, 0, 0], 0))
    print(number_of_pairs([1, 2, 3, 4, 5], [0, 0, 0, 0, 0], 0))
    print(number_of_pairs([10000, -10000], [-10000, 10000], -10000))
    print(number_of_pairs([-10000, 10000], [10000, -10000], 10000))
    a = random_nums(10000, 10000)
    b = random_nums(10000, 10000)
    print(f"{number_of_pairs(a, b, -100)} {number_of_pairs(a, b, 0)} {number_of_pairs(a, b, 10000)}")
    c = random_nums(10000, 3)
    d = random_nums(10000, 3)
    print(number_of_pairs(c, d, 0))
    check = 0
    total = 0
    for _ in range(3000):
        n = 2 + next_random() % 11
        x = random_nums(n, 5)
        y = random_nums(n, 5)
        diff = next_random() % 11 - 5
        answer = number_of_pairs(x, y, diff)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
