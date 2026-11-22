# LeetCode #2736: Maximum Sum Queries -- the bench (queries.kara in
# Python): pairs and queries by nums1 and x falling, a stack of (nums2,
# sum) with nums2 rising and sums falling, and a binary search per query.


def maximum_sum_queries(nums1, nums2, queries):
    n = len(nums1)
    pairs = sorted(zip(nums1, nums2), key=lambda p: -p[0])
    order = sorted(range(len(queries)), key=lambda q: -queries[q][0])
    answer = [-1] * len(queries)
    stack = []
    j = 0
    for q in order:
        x, y = queries[q]
        while j < n and pairs[j][0] >= x:
            a, b = pairs[j]
            j += 1
            if stack and stack[-1][0] >= b:
                continue
            while stack and stack[-1][1] <= a + b:
                stack.pop()
            stack.append((b, a + b))
        low, high = 0, len(stack)
        while low < high:
            middle = (low + high) // 2
            if stack[middle][0] >= y:
                high = middle
            else:
                low = middle + 1
        if low < len(stack):
            answer[q] = stack[low][1]
    return answer


seed = 2736


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_up_to(most):
    return (next_random() * 32768 + next_random()) % most + 1


def main():
    cases, n, rounds = 10, 100000, 3
    problems = []
    for _ in range(cases):
        nums1 = [random_up_to(1000000000) for _ in range(n)]
        nums2 = [random_up_to(1000000000) for _ in range(n)]
        queries = [[random_up_to(1000000000), random_up_to(1000000000)] for _ in range(n)]
        problems.append((nums1, nums2, queries))
    total = 0
    check = 0
    for r in range(rounds):
        for nums1, nums2, queries in problems:
            for best in maximum_sum_queries(nums1, nums2, queries):
                total += best
                check = (check * 31 + best + 1 + r) % 1000000007
    print(f"{cases} cases of {n} pairs and queries, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
