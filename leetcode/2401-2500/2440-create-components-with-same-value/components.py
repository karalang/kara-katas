# LeetCode #2440: Create Components With Same Value -- Python mirror of
# the ★ arm (components.kara): for each component count `k` dividing the
# total, from `n` down, the subtree sums gathered in reverse
# breadth-first order, each reaching the target cut off.


def fits(order, parent, nums, target):
    s = nums[:]
    for u in reversed(order):
        if s[u] > target:
            return False
        if s[u] < target:
            if u == 0:
                return False
            s[parent[u]] += s[u]
    return True


def component_value(nums, edges):
    n = len(nums)
    adjacent = [[] for _ in range(n)]
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
    parent = [-1] * n
    order = [0]
    seen = [False] * n
    seen[0] = True
    head = 0
    while head < len(order):
        u = order[head]
        head += 1
        for v in adjacent[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                order.append(v)
    total = sum(nums)
    for k in range(n, 1, -1):
        if total % k == 0 and fits(order, parent, nums, total // k):
            return k - 1
    return 0


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    edges = []
    for i in range(1, n):
        p = next_random() % i
        if next_random() % 2 == 0:
            edges.append([p, i])
        else:
            edges.append([i, p])
    for i in range(1, len(edges)):
        j = next_random() % (i + 1)
        edges[i], edges[j] = edges[j], edges[i]
    return edges


def main():
    global seed
    print(f"example 1: {component_value([6, 2, 2, 2, 6], [[0, 1], [1, 2], [1, 3], [3, 4]])}")
    print(f"example 2: {component_value([2], [])}")
    n = 10000
    path = [[i - 1, i] for i in range(1, n)]
    print(f"path of 1s: {component_value([1] * n, path)}")
    ends = [50] * n
    ends[0] = 1
    ends[n - 1] = 1
    print(f"path of 50s, 1 at each end: {component_value(ends, path)}")
    seed = 2440
    print(f"random tree of 5s: {component_value([5] * n, random_tree(n))}")
    values = [1 + next_random() % 50 for _ in range(n)]
    print(f"random tree, random values: {component_value(values, random_tree(n))}")
    star = [[0, i] for i in range(1, n)]
    twos = [2] * n
    twos[0] = 50
    print(f"star of 2s round 50: {component_value(twos, star)}")
    check = 0
    total = 0
    for _ in range(3000):
        size = 1 + next_random() % 10
        nums = [1 + next_random() % 4 for _ in range(size)]
        answer = component_value(nums, random_tree(size))
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
