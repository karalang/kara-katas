# LeetCode #1519: Number of Nodes in the Sub-Tree With the Same Label --
# the Python mirror of the ★ arm (labels.kara): a depth-first walk that
# returns each subtree's letter counts.
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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def show(answer):
    return "[" + ",".join(str(x) for x in answer) + "]"


def batch(count, most, letters):
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        edges = []
        for i in range(1, n):
            parent = (next_random() * 32768 + next_random()) % i
            if next_random() % 2 == 0:
                edges.append((parent, i))
            else:
                edges.append((i, parent))
        for i in range(len(edges) - 1, 0, -1):
            j = next_random() % (i + 1)
            edges[i], edges[j] = edges[j], edges[i]
        labels = "".join(chr(97 + next_random() % letters) for _ in range(n))
        for x in count_sub_trees(n, edges, labels):
            check = mix(check, x)
    return check


def main():
    global seed
    print(f"example 1 -> {show(count_sub_trees(7, [(0, 1), (0, 2), (1, 4), (1, 5), (2, 3), (2, 6)], 'abaedcd'))}")
    print(f"example 2 -> {show(count_sub_trees(4, [(0, 1), (1, 2), (0, 3)], 'bbbb'))}")
    print(f"example 3 -> {show(count_sub_trees(5, [(0, 1), (0, 2), (1, 3), (0, 4)], 'aabab'))}")
    print(f"one node -> {show(count_sub_trees(1, [], 'z'))}")
    seed = 1519
    print(f"2000 trees of 1 to 12 nodes over 3 letters: checksum {batch(2000, 12, 3)}")
    print(f"20 trees of 1 to 20000 nodes over 26 letters: checksum {batch(20, 20000, 26)}")


main()
