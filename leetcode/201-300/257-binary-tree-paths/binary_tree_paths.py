"""LeetCode 257 - Binary Tree Paths. Python oracle.

Mirrors binary_tree_paths.kara algorithm-for-algorithm: the same index-pool tree
built from a level-order array, and a DFS that extends a string prefix at every
node, finishing a path only at a node with NEITHER child.
"""

NULL = -1000


def build(vals, null_val):
    nodes = []
    n = len(vals)
    if n == 0 or vals[0] == null_val:
        return nodes
    nodes.append([vals[0], -1, -1])
    queue = [0]
    head = 0
    i = 1
    while head < len(queue) and i < n:
        cur = queue[head]
        head += 1
        if i < n and vals[i] != null_val:
            nodes.append([vals[i], -1, -1])
            nodes[cur][1] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
        if i < n and vals[i] != null_val:
            nodes.append([vals[i], -1, -1])
            nodes[cur][2] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
    return nodes


def binary_tree_paths(vals, null_val=NULL):
    out = []
    nodes = build(vals, null_val)
    if not nodes:
        return out

    def walk(node, prefix):
        left, right = nodes[node][1], nodes[node][2]
        if left == -1 and right == -1:
            out.append(prefix)
            return
        if left != -1:
            walk(left, prefix + "->" + str(nodes[left][0]))
        if right != -1:
            walk(right, prefix + "->" + str(nodes[right][0]))

    walk(0, str(nodes[0][0]))
    return out


def render(paths):
    return "[" + ",".join(paths) + "]" if paths else "[]"


def main():
    cases = [
        ([1, 2, 3, NULL, 5], "[1,2,3,null,5]"),
        ([1], "[1]"),
        ([], "[]"),
        ([1, 2], "[1,2]"),
        ([1, NULL, 2], "[1,null,2]"),
        ([1, 2, 3, 4, 5, 6, 7], "[1,2,3,4,5,6,7]"),
        ([1, 2, NULL, 3, NULL, 4, NULL], "[left spine 1-2-3-4]"),
        ([-1, -2, -3], "[-1,-2,-3]"),
        ([0, 0, 0], "[0,0,0]"),
    ]
    for vals, label in cases:
        print(f"{label} -> {render(binary_tree_paths(vals))}")


if __name__ == "__main__":
    main()
