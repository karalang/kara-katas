# LeetCode #2826: Sorting Three Groups -- the Python mirror of the ★ arm:
# a three-state table of the most numbers kept so far ending at a value
# at most v.


def minimum_operations(nums):
    best = [0, 0, 0]
    for x in nums:
        v = x - 1
        best[v] += 1
        for w in range(v + 1, 3):
            best[w] = max(best[w], best[v])
    return len(nums) - best[2]


# ---- the harness: the same in every arm --------------------------------

seed = 2826


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(minimum_operations([2, 1, 3, 2, 1]))
    print(minimum_operations([1, 3, 2, 1, 3, 3]))
    print(minimum_operations([2, 2, 2, 2, 3, 3]))
    print(minimum_operations([3]))
    print(minimum_operations([3 - i * 3 // 100 for i in range(100)]))
    print(minimum_operations([1 + i * 3 // 100 for i in range(100)]))
    total = 0
    check = 0
    for _ in range(5000):
        n = next_random() % 100 + 1
        nums = [next_random() % 3 + 1 for _ in range(n)]
        a = minimum_operations(nums)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"5000 arrays: {total} removals, checksum {check}")


main()
