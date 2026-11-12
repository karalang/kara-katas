# LeetCode #1133: Largest Unique Number -- the Python mirror of the ★ arm:
# every value from 0 to 1000 counted in a list, then the counts read from
# 1000 down for the first value seen exactly once.


def largest_unique_number(nums):
    count = [0] * 1001
    for x in nums:
        count[x] += 1
    for v in range(1000, -1, -1):
        if count[v] == 1:
            return v
    return -1


seed = 1133


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


def main():
    cases = [
        [5, 7, 3, 9, 4, 9, 8, 3, 1],
        [9, 9, 8, 8],
        [0],
        [1000],
        [1000, 1000, 0],
        [4, 4, 4],
        [2, 1, 2, 3, 3, 1, 0],
        [7, 3, 7, 3, 5, 6, 6],
    ]
    for nums in cases:
        print(f"{show(nums)} -> {largest_unique_number(nums)}")
    tops = [5, 31, 1001]
    total = 0
    none = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 60 + 1
        top = tops[next_random() % 3]
        nums = [next_random() % top for _ in range(n)]
        r = largest_unique_number(nums)
        total += r
        if r == -1:
            none += 1
        check = (check * 31 + r + 1) % 1000000007
    print(f"2000 random arrays: answers total {total}, {none} with none, checksum {check}")
    big = [next_random() % 1001 for _ in range(2000)]
    print(f"2000 random values: {largest_unique_number(big)}")
    twice = [i % 1000 for i in range(2000)]
    print(f"every value twice: {largest_unique_number(twice)}")


main()
