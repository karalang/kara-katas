# LeetCode #2226: Maximum Candies Allocated to K Children -- the
# benchmark's Python mirror of candies.kara: a binary search on the
# answer, x candies each possible when the piles give k shares of x.


def maximum_candies(candies, k):
    low = 0
    high = max(candies)
    while low < high:
        x = (low + high + 1) // 2
        shares = 0
        for pile in candies:
            shares += pile // x
        if shares >= k:
            low = x
        else:
            high = x - 1
    return low


seed = 2226


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    lists = [[wide_random() % 10000000 + 1 for _ in range(100000)] for _ in range(4)]
    children = [1000, 1000000, 1000000000, 100000000000]
    check = 0
    for _ in range(25):
        for l in range(4):
            # punch: one pile is drawn again before each answer
            at = wide_random() % 100000
            lists[l][at] = wide_random() % 10000000 + 1
            check = (check * 31 + maximum_candies(lists[l], children[l])) % 1000000007
    print(f"100 answers over 10^5 piles: checksum {check}")


main()
