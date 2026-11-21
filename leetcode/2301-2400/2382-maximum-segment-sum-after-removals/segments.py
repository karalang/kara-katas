# LeetCode #2382: Maximum Segment Sum After Removals -- Python mirror of
# the ★ arm, the removals undone in reverse with a union-find.


def find(parent, x):
    root = x
    while parent[root] != root:
        parent[root] = parent[parent[root]]
        root = parent[root]
    return root


def join(parent, total, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra != rb:
        parent[ra] = rb
        total[rb] += total[ra]


def maximum_segment_sum(nums, remove_queries):
    n = len(nums)
    parent = list(range(n))
    total = [0] * n
    back = [False] * n
    answer = [0] * n
    best = 0
    for k in range(n - 1, 0, -1):
        x = remove_queries[k]
        back[x] = True
        total[x] = nums[x]
        if x > 0 and back[x - 1]:
            join(parent, total, x - 1, x)
        if x + 1 < n and back[x + 1]:
            join(parent, total, x + 1, x)
        best = max(best, total[find(parent, x)])
        answer[k - 1] = best
    return answer


seed = 2382


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


def shuffled(n):
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    return order


def main():
    print(maximum_segment_sum([1, 2, 5, 6, 1], [0, 3, 2, 4, 1]))
    print(maximum_segment_sum([3, 2, 11, 1], [3, 2, 1, 0]))
    print(maximum_segment_sum([7], [0]))
    n = 3000
    big = [1000000000] * n
    left = list(range(n))
    outward = [n // 2 + i // 2 if i % 2 == 0 else n // 2 - 1 - i // 2 for i in range(n)]
    values = [1 + wide() % 1000000000 for _ in range(n)]
    order = shuffled(n)
    print(f"{fold(0, maximum_segment_sum(big, left))} {fold(0, maximum_segment_sum(big, outward))} {fold(0, maximum_segment_sum(values, order))}")
    check = 0
    firsts = 0
    for _ in range(2000):
        length = 1 + next_random() % 40
        top = 1 + wide() % 1000000000
        nums = [1 + wide() % top for _ in range(length)]
        queries = shuffled(length)
        answer = maximum_segment_sum(nums, queries)
        check = fold(check, answer)
        firsts += answer[0]
    print(f"2000 arrays: checksum {check}, first answers summing to {firsts}")


main()
