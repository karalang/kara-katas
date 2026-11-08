# LeetCode #2003: Smallest Missing Genetic Value in Each Subtree -- the
# mirror of the ★ arm, genetic.kara; its output is byte-identical.
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


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def fold(answer):
    total = check = 0
    for a in answer:
        total += a
        check = mix(check, a)
    return total, check


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([-1, 0, 0, 2], [1, 2, 3, 4]),
        ([-1, 0, 1, 0, 3, 3], [5, 4, 6, 2, 1, 3]),
        ([-1, 2, 3, 0, 2, 4, 1], [2, 3, 4, 5, 6, 7, 8]),
        ([-1], [1]),
        ([-1], [7]),
        ([-1, 0, 1, 2, 3], [5, 4, 3, 2, 1]),
        ([-1, 0, 0, 0, 0], [3, 1, 2, 5, 4]),
    ]
    for parents, nums in examples:
        print(f"{show(parents)} {show(nums)} -> {show(smallest_missing(parents, nums))}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        parents, nums = random_tree(n, next_random() % 4 + 1, next_random() % 3)
        t, c = fold(smallest_missing(parents, nums))
        total += t
        check = mix(check, c)
    print(f"2000 trees of 1 to 12 nodes: sum {total}, checksum {check}")
    total = check = 0
    for a in range(8):
        parents, nums = random_tree(20000, [1, 2, 5, 20000][a % 4], a % 2)
        t, c = fold(smallest_missing(parents, nums))
        total += t
        check = mix(check, c)
    print(f"8 trees of 20000 nodes: sum {total}, checksum {check}")


main()
