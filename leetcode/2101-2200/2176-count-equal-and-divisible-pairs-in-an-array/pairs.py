# LeetCode #2176: Count Equal and Divisible Pairs in an Array -- the
# Python mirror of pairs.kara: every pair of indices tried.


def count_pairs(nums, k):
    n = len(nums)
    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j] and i * j % k == 0:
                pairs += 1
    return pairs


# ---- test harness ---------------------------------------------------------

seed = 2176


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums, k):
    print(f"[{', '.join(map(str, nums))}], {k} -> {count_pairs(nums, k)}")


def main():
    show([3, 1, 2, 2, 2, 1, 3], 2)
    show([1, 2, 3, 4], 1)
    show([5], 3)
    show([4, 4], 7)
    show([7, 9, 9, 7, 9], 5)
    show([6, 6, 6, 6, 6], 1)
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 30 + 1
        k = next_random() % 12 + 1
        top = [3, 10][rnd % 2]
        nums = [next_random() % top + 1 for _ in range(n)]
        pairs = count_pairs(nums, k)
        total += pairs
        check = (check * 31 + pairs + k) % 1000000007
    print(f"2000 lists: {total} in all, checksum {check}")
    same = [1] * 100
    mixed = [next_random() % 4 + 1 for _ in range(100)]
    print(f"100 numbers: {count_pairs(same, 1)} {count_pairs(same, 100)} {count_pairs(mixed, 6)}")


main()
