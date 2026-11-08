# LeetCode #2003: Smallest Missing Genetic Value in Each Subtree -- the
# benchmark's Python twin, the same algorithm as genetic.kara here.
import sys

sys.setrecursionlimit(1000000)


def smallest_missing(parents, nums):
    n = len(parents)
    answer = [1] * n
    one = -1
    for i in range(n):
        if nums[i] == 1:
            one = i
    if one == -1:
        return answer
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parents[i]].append(i)
    seen = [False] * (n + 2)
    visited = [False] * n

    def mark(u):
        visited[u] = True
        if nums[u] <= n + 1:
            seen[nums[u]] = True
        for c in children[u]:
            if not visited[c]:
                mark(c)

    missing = 1
    u = one
    while u != -1:
        mark(u)
        while seen[missing]:
            missing += 1
        answer[u] = missing
        u = parents[u]
    return answer


seed = 2003


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# `n` nodes, each parent among the `width` nodes before it; the values a
# shuffle of 1..n + extra, the first n of them.
def random_tree(n, width, extra):
    parents = [-1]
    for i in range(1, n):
        lo = max(0, i - width)
        parents.append(lo + next_random() % (i - lo))
    values = list(range(1, n + extra + 1))
    for i in range(len(values) - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    return parents, values[:n]


def main():
    # 40 trees of 20000 nodes built once, then the ★ arm on each, 25 rounds
    trees = []
    for a in range(40):
        width = [2, 5, 50, 20000][a % 4]
        trees.append(random_tree(20000, width, a % 2))
    calls = total = check = 0
    for _ in range(25):
        for parents, nums in trees:
            answer = smallest_missing(parents, nums)
            calls += 1
            for a in answer:
                total += a
                check = (check * 31 + a) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
