"""LeetCode 257 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same spine-biased generator, the
same three path builders, and the same ORDER-SENSITIVE positional digest.

The digest is positional on purpose: the iterative builder's correctness depends
on pushing the right child before the left, and getting that backwards yields the
right SET of paths in reversed order. A sorted-set comparison would miss it.
"""
import sys

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


def make_case(seed, null_val):
    state = seed
    out = []
    state = (state * 1103515245 + 12345) & 2147483647
    slots = (state // 65536) % 26
    if slots == 0:
        return out
    state = (state * 1103515245 + 12345) & 2147483647
    spine = (state // 65536) % 3 == 0

    state = (state * 1103515245 + 12345) & 2147483647
    out.append((state // 65536) % 41 - 20)

    for s in range(1, slots):
        state = (state * 1103515245 + 12345) & 2147483647
        roll = (state // 65536) % 100
        want_null = (s % 2 == 0) if spine else (roll < 55)
        if want_null:
            out.append(null_val)
        else:
            state = (state * 1103515245 + 12345) & 2147483647
            out.append((state // 65536) % 41 - 20)
    return out


def paths_str(nodes):
    out = []
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


def paths_join(nodes):
    out = []
    if not nodes:
        return out
    path = []

    def walk(node):
        path.append(nodes[node][0])
        left, right = nodes[node][1], nodes[node][2]
        if left == -1 and right == -1:
            out.append("->".join(str(x) for x in path))
        else:
            if left != -1:
                walk(left)
            if right != -1:
                walk(right)
        path.pop()

    walk(0)
    return out


def paths_iter(nodes):
    out = []
    if not nodes:
        return out
    stack = [(0, str(nodes[0][0]))]
    while stack:
        node, prefix = stack.pop()
        left, right = nodes[node][1], nodes[node][2]
        if left == -1 and right == -1:
            out.append(prefix)
        else:
            # right first: LIFO, so the left child pops first
            if right != -1:
                stack.append((right, prefix + "->" + str(nodes[right][0])))
            if left != -1:
                stack.append((left, prefix + "->" + str(nodes[left][0])))
    return out


def digest_of(paths):
    h = 1
    for p in paths:
        for b in p.encode():
            h = (h * 1000003 + b) % 1000000007
        h = (h * 31 + 7) % 1000000007
    return h


def main():
    cases = 4000
    seed = 257257
    mismatches = total_paths = total_nodes = max_depth_seen = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & 2147483647
        vals = make_case(seed, NULL)
        nodes = build(vals, NULL)

        a = paths_str(nodes)
        b = paths_join(nodes)
        d = paths_iter(nodes)

        da = digest_of(a)
        if len(a) != len(b) or len(a) != len(d) or da != digest_of(b) or da != digest_of(d):
            mismatches += 1
        total_paths += len(a)
        total_nodes += len(nodes)
        for p in a:
            max_depth_seen = max(max_depth_seen, len(p.encode()))
        digest = (digest * 131 + da) % 1000000007

    print(f"cases {cases}")
    print(f"nodes {total_nodes}")
    print(f"paths {total_paths}")
    print(f"longest rendered path {max_depth_seen}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
