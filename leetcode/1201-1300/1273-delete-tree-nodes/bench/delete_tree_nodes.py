# LeetCode #1273 bench, in Python: the ★ arm (the children listed from the
# parents, then a depth-first search returning each subtree's sum and the
# nodes it keeps) on 20 random trees of 10,000 nodes with values from -3
# to 3, drawn once, 60 rounds; every answer folded into a checksum.
# The recursion can run deep, so it runs on a thread with a large stack.
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
    trees = []
    for _ in range(20):
        parent = random_parents(10000, 1000)
        value = [next_random() % 7 - 3 for _ in range(10000)]
        trees.append((parent, value))
    check = 0
    for rnd in range(60):
        for parent, value in trees:
            check = (check * 131 + delete_tree_nodes(10000, parent, value) + rnd) % 1000000007
    print(f"60 rounds of 20 trees of 10000 nodes: checksum {check}")


sys.setrecursionlimit(100000)
threading.stack_size(512 * 1024 * 1024)
t = threading.Thread(target=main)
t.start()
t.join()
