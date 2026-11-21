# LeetCode #1746: Maximum Subarray Sum After One Operation -- mirrors
# square.kara (the ★ arm).


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


def batch(count, most, top):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        nums = [next_random() % (2 * top + 1) - top for _ in range(n)]
        answer = max_sum_after_operation(nums)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{count} arrays of up to {most} values within {top}: sums add to {total}, checksum {check}")


for nums in [[2, -1, -4, -3], [1, -1, 1, 1, -1, -1, 1], [-7], [-3, -9, -2], [10000, -10000, 10000]]:
    print(max_sum_after_operation(nums))
batch(3000, 8, 5)
batch(300, 1000, 10000)
batch(10, 100000, 10000)
