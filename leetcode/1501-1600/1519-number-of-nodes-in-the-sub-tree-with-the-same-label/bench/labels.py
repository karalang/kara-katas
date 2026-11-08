# LeetCode #1519 bench: the ★ arm (counts returned up a recursive walk),
# as labels.kara.
import sys

sys.setrecursionlimit(100000)


def walk(node, parent, adjacent, labels, answer):
    counts = [0] * 26
    for nxt in adjacent[node]:
        if nxt != parent:
            below = walk(nxt, node, adjacent, labels, answer)
            for c in range(26):
                counts[c] += below[c]
    mine = labels[node] - 97
    counts[mine] += 1
    answer[node] = counts[mine]
    return counts


def count_sub_trees(n, edges, labels):
    adjacent = [[] for _ in range(n)]
    for a, b in edges:
        adjacent[a].append(b)
        adjacent[b].append(a)
    answer = [0] * n
    walk(0, -1, adjacent, labels.encode(), answer)
    return answer


seed = 1519


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 200000
    edges = []
    for i in range(1, n):
        edges.append(((next_random() * 32768 + next_random()) % i, i))
    labels = "".join(chr(97 + next_random() % 26) for _ in range(n))
    check = 0
    for _ in range(5):
        for x in count_sub_trees(n, edges, labels):
            check = (check * 31 + x + 1) % 1000000007
    print(f"5 passes over a tree of 200000 nodes: checksum {check}")


main()
