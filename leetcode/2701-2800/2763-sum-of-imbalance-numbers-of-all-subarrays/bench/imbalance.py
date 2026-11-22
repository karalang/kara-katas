# LeetCode #2763: Sum of Imbalance Numbers of All Subarrays -- the bench
# (imbalance.kara in Python): each index counted for the subarrays in
# which it is the leftmost occurrence of a run's top value, from the last
# x or x + 1 before it and the first x + 1 after it.


def sum_imbalance_numbers(nums):
    n = len(nums)
    left = [0] * n
    last = [-1] * (n + 2)
    for i, x in enumerate(nums):
        left[i] = max(last[x], last[x + 1])
        last[x] = i
    first = [n] * (n + 2)
    total = 0
    for i in range(n - 1, -1, -1):
        x = nums[i]
        total += (i - left[i]) * (first[x + 1] - i)
        first[x] = i
    return total - n * (n + 1) // 2


seed = 2763


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 20000, 5
    cases = [[next_random() % 1000 + 1 for _ in range(1000)] for _ in range(count)]
    total = check = 0
    for r in range(rounds):
        for nums in cases:
            found = sum_imbalance_numbers(nums)
            total += found
            check = (check * 31 + found + r) % 1000000007
    print(f"{count} arrays of 1000, {rounds} rounds: imbalances sum to {total}, checksum {check}")


main()
