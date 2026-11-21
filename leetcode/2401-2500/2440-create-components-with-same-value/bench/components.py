# LeetCode #2440: Create Components With Same Value -- the bench, the ★
# arm: each component count dividing the total, from `n` down, checked by
# gathering subtree sums in reverse breadth-first order.


def fits(order, parent, nums, target):
    s = nums[:]
    i = len(order)
    while i > 0:
        i -= 1
        u = order[i]
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
    for e in edges:
        adjacent[e[0]].append(e[1])
        adjacent[e[1]].append(e[0])
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
    total = 0
    for x in nums:
        total += x
    k = n
    while k > 1:
        if total % k == 0 and fits(order, parent, nums, total // k):
            return k - 1
        k -= 1
    return 0


seed = 2440


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 20000
    trees = []
    values = []
    for _ in range(10):
        edges = []
        for i in range(1, n):
            edges.append([next_random() % i, i])
        nums = [1 + next_random() % 50 for _ in range(n)]
        trees.append(edges)
        values.append(nums)
    check = 0
    for p in range(50):
        for c in range(len(trees)):
            at = (p * 7919 + c * 104729) % n
            values[c][at] = 1 + next_random() % 50
            check = (check * 31 + component_value(values[c], trees[c]) + p) % 1000000007
    print(f"50 passes over 10 trees of 2 * 10^4 nodes: checksum {check}")


main()
