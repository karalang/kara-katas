# LeetCode #2404: Most Frequent Even Element -- the Python mirror of the
# ★ arm: a dict of counts of the even values, the most frequent and the
# smallest among equal counts.

seed = 2404


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def most_frequent_even(nums):
    count = {}
    for x in nums:
        if x % 2 == 0:
            count[x] = count.get(x, 0) + 1
    best = -1
    most = 0
    for x, c in count.items():
        if c > most or c == most and x < best:
            best = x
            most = c
    return best


def main():
    print(most_frequent_even([0, 1, 2, 2, 4, 4, 1]))
    print(most_frequent_even([4, 4, 4, 9, 2, 4]))
    print(most_frequent_even([29, 47, 21, 41, 13, 37, 25, 7]))
    print(f"{most_frequent_even([0])} {most_frequent_even([99999])}")
    print(most_frequent_even([8, 6, 6, 8, 100000, 100000, 3, 3, 3]))
    wide = []
    for _ in range(2000):
        hi = next_random()
        wide.append((hi * 32768 + next_random()) % 100001)
    print(most_frequent_even(wide))
    narrow = []
    for _ in range(2000):
        x = next_random()
        narrow.append(2 * (1 + x // 2 % 10) if x % 2 == 0 else x)
    print(most_frequent_even(narrow))
    check = 0
    none = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 40
        nums = [next_random() % top for _ in range(n)]
        a = most_frequent_even(nums)
        if a < 0:
            none += 1
        check = (check * 31 + a + 1) % 1000000007
    print(f"3000 random: checksum {check}, {none} with no even")


if __name__ == "__main__":
    main()
