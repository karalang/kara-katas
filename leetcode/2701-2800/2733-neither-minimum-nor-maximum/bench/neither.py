# LeetCode #2733: Neither Minimum nor Maximum -- the bench (neither.kara
# in Python): the least and the greatest in one pass, then the first
# number that is neither.


def find_non_min_or_max(nums):
    low = high = nums[0]
    for x in nums:
        low = min(low, x)
        high = max(high, x)
    for x in nums:
        if x != low and x != high:
            return x
    return -1


seed = 2733


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 2000, 3000
    arrays = []
    for _ in range(count):
        n = next_random() % 100 + 1
        every = list(range(1, 101))
        for i in range(99, 0, -1):
            j = next_random() % (i + 1)
            every[i], every[j] = every[j], every[i]
        arrays.append(every[:n])
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            answer = find_non_min_or_max(nums)
            total += answer
            check = (check * 31 + answer + 1 + r) % 1000000007
    print(f"{count} arrays, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
