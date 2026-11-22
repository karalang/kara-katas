# LeetCode #2736: Maximum Sum Queries -- Python mirror of queries.kara
# (the ★ arm): pairs and queries by nums1 and x falling, a stack of
# (nums2, sum) with nums2 rising and sums falling, and a binary search.


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


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    print(show(maximum_sum_queries([4, 3, 1, 2], [2, 4, 9, 5], [[4, 1], [1, 3], [2, 5]])))
    print(show(maximum_sum_queries([3, 2, 5], [2, 3, 4], [[4, 4], [3, 2], [1, 1]])))
    print(show(maximum_sum_queries([2, 1], [2, 3], [[3, 3]])))
    total = 0
    check = 0
    for c in range(1010):
        if c < 1000:
            n, q, most = next_random() % 20 + 1, next_random() % 20 + 1, 30
        else:
            n, q, most = 2000, 2000, 1000000000
        nums1 = [random_up_to(most) for _ in range(n)]
        nums2 = [random_up_to(most) for _ in range(n)]
        queries = [[random_up_to(most), random_up_to(most)] for _ in range(q)]
        for best in maximum_sum_queries(nums1, nums2, queries):
            total += best
            check = (check * 31 + best + 1) % 1000000007
        if c == 999:
            print(f"1000 small cases: answers sum to {total}, checksum {check}")
            total = 0
            check = 0
    print(f"10 cases of 2000 pairs: answers sum to {total}, checksum {check}")


main()
