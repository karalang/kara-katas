# LeetCode #1749: Maximum Absolute Sum of Any Subarray -- the bench
# (abs.kara in Python): Kadane's scan both ways.


def max_absolute_sum(nums):
    high = 0
    low = 0
    best = 0
    for x in nums:
        high = max(high, 0) + x
        low = min(low, 0) + x
        best = max(best, max(high, -low))
    return best


seed = 1749


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds, n = 20, 40, 100000
arrays = [[next_random() % 20001 - 10000 for _ in range(n)] for _ in range(count)]
total = 0
check = 0
for r in range(rounds):
    for nums in arrays:
        answer = max_absolute_sum(nums)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} arrays of {n} values, {rounds} rounds: answers add to {total}, checksum {check}")
