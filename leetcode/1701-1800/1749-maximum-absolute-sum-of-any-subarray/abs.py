# LeetCode #1749: Maximum Absolute Sum of Any Subarray -- mirrors
# abs.kara (the ★ arm).


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


def batch(count, most, top):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        nums = [next_random() % (2 * top + 1) - top for _ in range(n)]
        answer = max_absolute_sum(nums)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} arrays of up to {most} values within {top}: answers add to {total}, checksum {check}")


for nums in [[1, -3, 2, 3, -4], [2, -5, 1, -4, 3, -2], [-7], [-3, -9, -2], [-10000] * 100000]:
    print(max_absolute_sum(nums))
batch(3000, 8, 5)
batch(300, 1000, 10000)
batch(10, 100000, 10000)
