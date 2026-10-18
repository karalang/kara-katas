# LeetCode #724: Find Pivot Index -- the total, then one running sum.
#
# A mirror of find_pivot_index.kara (the ★ arm) and its harness.


def pivot_index(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_nums(n, top, seed):
    return [next_random(seed) % (2 * top + 1) - top for _ in range(n)]


def show(nums):
    print(f"{nums} -> {pivot_index(nums)}")


def main():
    show([1, 7, 3, 6, 5, 6])
    show([1, 2, 3])
    show([2, 1, -1])
    show([0])
    show([5])
    show([0, 0, 0])
    show([1, -1])
    show([-1, -1, -1, 0, 1, 1])
    show([3, 5, -2, 1, 1, 9, -6, 3])
    show([1, 2, 3, 4, 0, 6])
    seed = [724]
    big = random_nums(10000, 1000, seed)
    print(f"10000 random numbers -> {pivot_index(big)}")
    half = random_nums(5000, 1000, seed)
    balanced = half + half[:4999][::-1]
    print(f"9999 numbers that balance -> {pivot_index(balanced)}")
    print(f"10000 zeros -> {pivot_index([0] * 10000)}")
    total = 0
    found = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 12
        top = next_random(seed) % 4
        p = pivot_index(random_nums(n, top, seed))
        if p >= 0:
            found += 1
        total = (total * 131 + p + 1) % 1000000007
    print(f"300 random arrays: {found} with a pivot, checksum {total}")


main()
