# LeetCode #2382: Maximum Segment Sum After Removals -- the bench, the ★
# arm in Python: the removals undone in reverse with a union-find, each
# root keeping its segment's sum.


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


def main():
    # 10 arrays of 10^5 values, array a's values from 1 to 10^a, each with
    # its own random order of removals
    n = 100000
    arrays = []
    orders = []
    for a in range(10):
        top = 10 ** a
        arrays.append([1 + wide() % top for _ in range(n)])
        order = list(range(n))
        for i in range(n - 1, 0, -1):
            j = wide() % (i + 1)
            order[i], order[j] = order[j], order[i]
        orders.append(order)
    check = 0
    for p in range(10):
        for a in range(10):
            for v in maximum_segment_sum(arrays[a], orders[a]):
                check = (check * 31 + v + p) % 1000000007
    print(f"10 passes over 10 arrays of 10^5 values: checksum {check}")


main()
