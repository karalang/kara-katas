# LeetCode #1748: Sum of Unique Elements -- the bench (unique.kara in
# Python): one pass with a state per value.


def sum_of_unique(nums):
    seen = [0] * 101
    total = 0
    for x in nums:
        if seen[x] == 0:
            total += x
        elif seen[x] == 1:
            total -= x
        seen[x] = min(seen[x] + 1, 2)
    return total


seed = 1748


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


count, rounds, n = 50000, 10, 100
arrays = [[next_random() % 100 + 1 for _ in range(n)] for _ in range(count)]
total = 0
check = 0
for r in range(rounds):
    for nums in arrays:
        answer = sum_of_unique(nums)
        total += answer
        check = (check * 31 + answer + r) % 1000000007
print(f"{count} arrays of {n} values, {rounds} rounds: unique sums add to {total}, checksum {check}")
