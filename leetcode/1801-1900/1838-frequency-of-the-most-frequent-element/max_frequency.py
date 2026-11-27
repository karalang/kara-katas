# LeetCode #1838: Frequency of the Most Frequent Element -- the ★ arm in
# Python


def max_frequency(nums, k):
    s = sorted(nums)
    best = 0
    first = 0
    total = 0
    for last in range(len(s)):
        total += s[last]
        while s[last] * (last - first + 1) - total > k:
            total -= s[first]
            first += 1
        best = max(best, last - first + 1)
    return best


seed = 1838


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{max_frequency([1, 2, 4], 5)} {max_frequency([1, 4, 8, 13], 5)} {max_frequency([3, 9, 6], 2)}")
    print(f"{max_frequency([7], 1)} {max_frequency([5, 5, 5], 1)} {max_frequency([1, 3, 5], 1)} {max_frequency([1, 50000, 100000], 199999)} {max_frequency([1, 1, 10, 10], 8)}")
    nums = [1 + (next_random() * 32768 + next_random()) % 100000 for _ in range(100000)]
    print(f"the most: {max_frequency(nums, 100000)} {max_frequency(nums, 1)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 10
        case = [1 + next_random() % 20 for _ in range(n)]
        k = 1 + next_random() % 30
        check = (check * 31 + max_frequency(case, k)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
