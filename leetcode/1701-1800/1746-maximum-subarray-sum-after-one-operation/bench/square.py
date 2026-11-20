# LeetCode #1746: Maximum Subarray Sum After One Operation -- the bench
# (square.kara in Python): Kadane's scan with two states.


def max_sum_after_operation(nums):
    plain = 0
    squared = 0
    best = -(2**31)
    for x in nums:
        squared = max(squared + x, max(plain, 0) + x * x)
        plain = max(plain, 0) + x
        best = max(best, squared)
    return best


seed = 1746


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
        answer = max_sum_after_operation(nums)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} arrays of {n} values, {rounds} rounds: sums add to {total}, checksum {check}")
