# LeetCode #2098: Subsequence of Size K With the Largest Even Sum -- Python
# mirror of the ★ arm (even_sum.kara): the k largest numbers, and when
# their sum is odd the better of two swaps across the parities.


def largest_even_sum(nums, k):
    s = sorted(nums, reverse=True)
    total = sum(s[:k])
    if total % 2 == 0:
        return total
    taken_odd = min((x for x in s[:k] if x % 2 == 1), default=None)
    taken_even = min((x for x in s[:k] if x % 2 == 0), default=None)
    left_odd = max((x for x in s[k:] if x % 2 == 1), default=None)
    left_even = max((x for x in s[k:] if x % 2 == 0), default=None)
    best = -1
    if taken_odd is not None and left_even is not None:
        best = max(best, total - taken_odd + left_even)
    if taken_even is not None and left_odd is not None:
        best = max(best, total - taken_even + left_odd)
    return best


# ---- test harness -----------------------------------------------------------

seed = 2098


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def show(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


examples = [
    ([4, 1, 5, 3, 1], 3),
    ([4, 6, 2], 3),
    ([1, 3, 5], 1),
    ([7], 1),
    ([0], 1),
    ([5, 5, 2, 9, 1], 2),
    ([9, 8, 1], 2),
    ([3, 3, 3, 3, 3], 5),
]
for nums, k in examples:
    print(f"{show(nums)} k={k} -> {largest_even_sum(nums, k)}")
none = 0
check = 0
for round_ in range(3000):
    n = next_random() % 30 + 1
    top = [10, 100, 100001][round_ % 3]
    nums = [wide_random() % top for _ in range(n)]
    k = next_random() % n + 1
    got = largest_even_sum(nums, k)
    if got < 0:
        none += 1
    check = (check * 31 + got + 1) % 1000000007
print(f"3000 lists: {none} with no even sum, checksum {check}")
n = 100000
nums = [wide_random() % 100001 for _ in range(n)]
for k in [1, 50001, 100000]:
    print(f"100000 random, k={k}: {largest_even_sum(nums, k)}")
odd = [2 * (i % 50000) + 1 for i in range(n)]
print(f"100000 odd, k=99999: {largest_even_sum(odd, 99999)}, k=100000: {largest_even_sum(odd, 100000)}")
same = [100000] * n
print(f"100000 of 100000, k=100000: {largest_even_sum(same, 100000)}")
