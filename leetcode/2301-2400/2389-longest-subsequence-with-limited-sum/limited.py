# LeetCode #2389: Longest Subsequence With Limited Sum -- the Python mirror
# of limited.kara.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def fold(check, values):
    for v in values:
        check = (check * 31 + v) % 1000000007
    return check


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    global seed
    print(show(answer_queries([4, 5, 2, 1], [3, 10, 21])))
    print(show(answer_queries([2, 3, 4, 5], [1])))
    print(show(answer_queries([7, 1, 3], [0, 11, 100])))
    print(show(answer_queries([5, 5, 5, 5], [4, 5, 9, 10, 15, 19, 20, 21])))
    seed = 2389
    nums = [1 + wide() % 1000000 for _ in range(1000)]
    queries = [1 + wide() % 1000000000 for _ in range(1000)]
    print(f"1000 queries: checksum {fold(0, answer_queries(nums, queries))}")
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        top = 1 + next_random() % 100
        nums = [1 + next_random() % top for _ in range(n)]
        m = 1 + next_random() % 10
        queries = [next_random() % (sum(nums) + 5) for _ in range(m)]
        answer = answer_queries(nums, queries)
        check = fold(check, answer)
        total += sum(answer)
    print(f"3000 arrays: checksum {check}, lengths summing to {total}")


if __name__ == "__main__":
    main()
