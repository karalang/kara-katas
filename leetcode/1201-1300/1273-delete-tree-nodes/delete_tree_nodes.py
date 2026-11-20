# LeetCode #1273: Delete Tree Nodes -- Python mirror of the ★ arm (the
# children listed, then a depth-first search returning each subtree's sum
# and the nodes it keeps), with the same harness. The recursion reaches
# 10^4 deep, so it runs on a thread with a large stack.
import sys
import threading


def subtree(node, children, value):
    total = value[node]
    kept = 1
    for child in children[node]:
        s, k = subtree(child, children, value)
        total += s
        kept += k
    return (0, 0) if total == 0 else (total, kept)


def delete_tree_nodes(nodes, parent, value):
    children = [[] for _ in range(nodes)]
    for i in range(1, nodes):
        children[parent[i]].append(i)
    return subtree(0, children, value)[1]


seed = 1273


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_parents(n, reach):
    order = list(range(n))
    for i in range(n - 1, 1, -1):
        j = 1 + next_random() % i
        order[i], order[j] = order[j], order[i]
    parent = [-1] * n
    for i in range(1, n):
        back = 1 + next_random() % min(reach, i)
        parent[order[i]] = order[i - back]
    return parent


def main():
    parent = [-1, 0, 0, 1, 2, 2, 2]
    print(f"{delete_tree_nodes(7, parent, [1, -2, 4, 0, -2, -1, -1])} {delete_tree_nodes(7, parent, [1, -2, 4, 0, -2, -1, -2])}")
    left = 0
    check = 0
    for case in range(2000):
        n = next_random() % 60 + 1
        reach = 1000 if case % 2 == 0 else 2
        parent = random_parents(n, reach)
        value = [next_random() % 7 - 3 for _ in range(n)]
        got = delete_tree_nodes(n, parent, value)
        left += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random trees: {left} nodes left, checksum {check}")
    path = [i - 1 for i in range(10000)]
    bush = random_parents(10000, 10000)
    deep = random_parents(10000, 3)
    wide = [next_random() % 200001 - 100000 for _ in range(10000)]
    alternating = [5 if i % 2 == 0 else -5 for i in range(10000)]
    print(f"{delete_tree_nodes(10000, path, alternating)} {delete_tree_nodes(10000, bush, wide)} {delete_tree_nodes(10000, deep, wide)} {delete_tree_nodes(10000, path, wide)}")


sys.setrecursionlimit(100000)
threading.stack_size(512 * 1024 * 1024)
t = threading.Thread(target=main)
t.start()
t.join()
