# LeetCode #2113: Elements in Array After Removing and Replacing Elements
# -- the Python mirror of elements.kara (the ★ arm): each query's minute
# modulo `2n`, then one value or -1 for its phase. O(q).


def element_in_nums(nums, queries):
    n = len(nums)
    ans = []
    for time, index in queries:
        t = time % (2 * n)
        if t < n:
            ans.append(nums[t + index] if index < n - t else -1)
        else:
            ans.append(nums[index] if index < t - n else -1)
    return ans


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    examples = [
        ([0, 1, 2], [(0, 2), (2, 0), (3, 2), (5, 0)]),
        ([2], [(0, 0), (1, 0), (2, 0), (3, 0)]),
        ([5, 6], [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)]),
        ([7, 8, 9, 10], [(4, 0), (8, 3), (7, 3), (6, 1), (100000, 3)]),
    ]
    for nums, queries in examples:
        print(f"{nums} at {queries} -> {element_in_nums(nums, queries)}")
    seed = [2113]
    total = 0
    check = 0
    missing = 0
    for _ in range(2000):
        n = next_random(seed) % 10 + 1
        nums = [next_random(seed) % 101 for _ in range(n)]
        q = next_random(seed) % 20 + 1
        queries = []
        for _ in range(q):
            t = next_random(seed) % 61
            i = next_random(seed) % n
            queries.append((t, i))
        for x in element_in_nums(nums, queries):
            if x == -1:
                missing += 1
            else:
                total += x
            check = (check * 31 + x + 1) % 1000000007
    print(f"2000 arrays: {total} summed, {missing} missing, checksum {check}")
    nums = [i * 7 % 101 for i in range(100)]
    queries = [(j, j * 37 % 100) for j in range(100000)]
    got = element_in_nums(nums, queries)
    found = sum(1 for x in got if x >= 0)
    total = sum(x for x in got if x >= 0)
    print(f"10^5 queries: {found} found, {total} summed")


main()
