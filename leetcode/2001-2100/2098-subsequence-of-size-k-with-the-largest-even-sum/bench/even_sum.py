# LeetCode #2098: Subsequence of Size K With the Largest Even Sum -- Python
# mirror of the ★ arm's benchmark (even_sum.kara): the same 200 lists of
# 100000 numbers, each sorted largest first and given the better swap.


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


seed = 2098


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


total = 0
check = 0
for _ in range(200):
    nums = [wide_random() % 100001 for _ in range(100000)]
    k = wide_random() % 100000 + 1
    got = largest_even_sum(nums, k)
    total += got
    check = (check * 31 + got + 1) % 1000000007
print(f"200 answers: sum {total}, checksum {check}")
