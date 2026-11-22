# LeetCode #2826: Sorting Three Groups -- the bench's Python mirror of
# the ★ arm: a three-state table of the most numbers kept so far ending
# at a value at most v.


def minimum_operations(nums):
    best = [0, 0, 0]
    for x in nums:
        v = x - 1
        best[v] += 1
        for w in range(v + 1, 3):
            best[w] = max(best[w], best[v])
    return len(nums) - best[2]


seed = 2826


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 200000, 5
    cases = [[next_random() % 3 + 1 for _ in range(100)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            a = minimum_operations(nums)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 100, {rounds} rounds: {total} removals, checksum {check}")


main()
