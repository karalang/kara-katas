# LeetCode #2389: Longest Subsequence With Limited Sum -- the bench, the
# ★ arm in Python: the values sorted into prefix sums, each query
# answered by binary search.


def answer_queries(nums, queries):
    prefix = []
    running = 0
    for v in sorted(nums):
        running += v
        prefix.append(running)
    answer = []
    for q in queries:
        low = 0
        high = len(prefix)
        while low < high:
            mid = (low + high) // 2
            if prefix[mid] <= q:
                low = mid + 1
            else:
                high = mid
        answer.append(low)
    return answer


seed = 2389


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def main():
    # 100 arrays of 1000 values up to 10^6, each with 1000 queries up to
    # 10^9; each pass answers them all and folds every answer
    arrays = []
    asks = []
    for _ in range(100):
        arrays.append([1 + wide() % 1000000 for _ in range(1000)])
        asks.append([1 + wide() % 1000000000 for _ in range(1000)])
    check = 0
    for p in range(200):
        for a in range(100):
            for v in answer_queries(arrays[a], asks[a]):
                check = (check * 31 + v + p) % 1000000007
    print(f"200 passes over 100 arrays of 1000 values and 1000 queries: checksum {check}")


main()
