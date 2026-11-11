# LeetCode #2113: Elements in Array After Removing and Replacing Elements
# -- the benchmark, the same algorithm as elements.kara: each query's
# minute modulo the period `2n`, then one value or -1 for its phase.


def element_in_nums(nums, queries):
    n = len(nums)
    ans = []
    for time, index in queries:
        t = time % (2 * n)
        if t < n:
            if index < n - t:
                ans.append(nums[t + index])
            else:
                ans.append(-1)
        elif index < t - n:
            ans.append(nums[index])
        else:
            ans.append(-1)
    return ans


seed = 2113


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(20):
        arrays.append([next_random() % 101 for _ in range(100)])
    queries = []
    for _ in range(100000):
        time = next_random() % 100001
        queries.append((time, next_random() % 100))
    total = 0
    check = 0
    for s in range(50):
        j = s * 1999 % 100000
        queries[j] = (queries[j][0] + 1, queries[j][1])
        total_s = sum(element_in_nums(arrays[s % 20], queries))
        total += total_s
        check = (check * 31 + total_s) % 1000000007
    print(f"50 solves: {total} summed, checksum {check}")


main()
