# LeetCode #698: Partition to K Equal Sum Subsets -- values into buckets.
#
# A mirror of can_partition_k_subsets.kara (the ★ arm) and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def place(nums, i, buckets, target):
    if i == len(nums):
        return True
    for b in range(len(buckets)):
        if buckets[b] + nums[i] > target:
            continue
        if any(buckets[c] == buckets[b] for c in range(b)):
            continue
        buckets[b] += nums[i]
        if place(nums, i + 1, buckets, target):
            return True
        buckets[b] -= nums[i]
    return False


def can_partition_k_subsets(nums, k):
    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k
    s = sorted(nums, reverse=True)
    if s[0] > target:
        return False
    return place(s, 0, [0] * k, target)


def yes_no(b):
    return "yes" if b else "no"


def random_problem():
    k = 1 + next_random() % 6
    target = 16 + next_random() % 9985
    nums = []
    for _ in range(k):
        g = 1 + next_random() % (16 // k)
        left = target
        for _ in range(g - 1):
            part = 1 + next_random() % (target // g)
            nums.append(part)
            left -= part
        nums.append(left)
    n = len(nums)
    for i in range(n):
        j = i + next_random() % (n - i)
        nums[i], nums[j] = nums[j], nums[i]
    if n >= 2 and next_random() % 2 == 0:
        i = next_random() % n
        j = (i + 1 + next_random() % (n - 1)) % n
        most = min(nums[j] - 1, 10000 - nums[i])
        if most >= 1:
            d = 1 + next_random() % most
            nums[i] += d
            nums[j] -= d
    return nums, k


def main():
    global seed
    f = can_partition_k_subsets
    print(f"example 1: {yes_no(f([4, 3, 2, 3, 5, 2, 1], 4))}")
    print(f"example 2: {yes_no(f([1, 2, 3, 4], 3))}")
    print(f"one subset: {yes_no(f([5, 1, 9], 1))}, sixteen of 7: {yes_no(f([7] * 16, 16))}, "
          f"odd total: {yes_no(f([1, 1, 1, 1, 1], 2))}, too big: {yes_no(f([9, 1, 1, 1], 2))}")
    a = f([2, 2, 2, 2, 3, 4, 5], 4)
    b = f([3, 3, 10, 2, 6, 5, 10, 6, 8, 3, 2, 1, 6, 10, 7, 2], 6)
    c = f([10, 10, 10, 7, 7, 7, 7, 7, 7, 6, 6, 6], 3)
    d = f([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4], 4)
    print(f"[2,2,2,2,3,4,5] in 4: {yes_no(a)}, sixteen in 6: {yes_no(b)}, twelve in 3: {yes_no(c)}, "
          f"1 to 4 four times in 4: {yes_no(d)}")
    big = [9999] * 16
    big[0] = 9997
    big[1] = 10000
    big[2] = 10000
    e = f(big, 8)
    big[0] = 9998
    big[2] = 9999
    g = f(big, 8)
    print(f"9997 among 9999s in 8: {yes_no(e)}, 9998 instead: {yes_no(g)}")
    seed = 698
    yes = 0
    checksum = 0
    for _ in range(300):
        nums, k = random_problem()
        r = f(nums, k)
        if r:
            yes += 1
        checksum = (checksum * 3 + (1 if r else 0) + len(nums)) % 1000000007
    print(f"300 random problems: {yes} can be split, checksum {checksum}")


main()
