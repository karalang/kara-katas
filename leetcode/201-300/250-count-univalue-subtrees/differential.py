"""LeetCode 250 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same draw order, same tree
generator, same four solvers, same aggregate report.

The PRNG stays in [0, 2^31) and every operand is non-negative, so Python's
floor-division/modulo and Kara's truncating pair agree throughout -- there is no
sign correction to get wrong here (unlike #249).
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
            li = len(nodes) - 1
            nodes[cur][1] = li
            queue.append(li)
        i += 1
        if i < n and vals[i] != null_val:
            nodes.append([vals[i], -1, -1])
            ri = len(nodes) - 1
            nodes[cur][2] = ri
            queue.append(ri)
        i += 1
    return nodes


def count_rec(nodes):
    """Post-order, iterative here only to dodge Python's recursion limit; the
    visit order and the non-short-circuit combining match the .kara recursion."""
    n = len(nodes)
    if n == 0:
        return 0
    uni = [False] * n
    total = 0
    stack = [(0, False)]
    while stack:
        node, expanded = stack.pop()
        if node == -1:
            continue
        if not expanded:
            stack.append((node, True))
            stack.append((nodes[node][2], False))
            stack.append((nodes[node][1], False))
            continue
        left, right = nodes[node][1], nodes[node][2]
        left_uni = True if left == -1 else uni[left]
        right_uni = True if right == -1 else uni[right]
        ok = left_uni and right_uni
        if left != -1 and nodes[left][0] != nodes[node][0]:
            ok = False
        if right != -1 and nodes[right][0] != nodes[node][0]:
            ok = False
        uni[node] = ok
        if ok:
            total += 1
    return total


def count_iter(nodes):
    return count_rec(nodes)  # same shape in Python; kept for symmetry of report


def count_scan(nodes):
    n = len(nodes)
    if n == 0:
        return 0
    uni = [False] * n
    total = 0
    for i in range(n - 1, -1, -1):
        left, right = nodes[i][1], nodes[i][2]
        ok = True
        if left != -1 and (not uni[left] or nodes[left][0] != nodes[i][0]):
            ok = False
        if right != -1 and (not uni[right] or nodes[right][0] != nodes[i][0]):
            ok = False
        uni[i] = ok
        if ok:
            total += 1
    return total


def count_pair(nodes):
    """Pure twin: (uni, count) returned upward instead of an accumulator."""
    n = len(nodes)
    if n == 0:
        return 0
    uni = [False] * n
    cnt = [0] * n
    for i in range(n - 1, -1, -1):
        left, right = nodes[i][1], nodes[i][2]
        lu = True if left == -1 else uni[left]
        ru = True if right == -1 else uni[right]
        ok = lu and ru
        if left != -1 and nodes[left][0] != nodes[i][0]:
            ok = False
        if right != -1 and nodes[right][0] != nodes[i][0]:
            ok = False
        uni[i] = ok
        cnt[i] = (0 if left == -1 else cnt[left]) + (0 if right == -1 else cnt[right]) + (1 if ok else 0)
    return cnt[0]


def main():
    null = NULL
    cases = 4000

    state = 20250250
    total_nodes = 0
    total_uni = 0
    all_uni_trees = 0
    mismatches = 0

    for _ in range(cases):
        state = (state * 1103515245 + 12345) % 2147483648
        slots = (state // 65536) % 48 + 1

        state = (state * 1103515245 + 12345) % 2147483648
        alphabet = (state // 65536) % 2 + 2

        vals = []
        for s in range(slots):
            state = (state * 1103515245 + 12345) % 2147483648
            roll = (state // 65536) % 100
            if s > 0 and roll < 28:
                vals.append(null)
            else:
                state = (state * 1103515245 + 12345) % 2147483648
                vals.append((state // 65536) % alphabet)

        nodes = build(vals, null)
        a = count_rec(nodes)
        b = count_iter(nodes)
        d = count_scan(nodes)
        e = count_pair(nodes)

        if a != b or a != d or a != e:
            mismatches += 1
        total_nodes += len(nodes)
        total_uni += a
        if len(nodes) > 0 and a == len(nodes):
            all_uni_trees += 1

    print(f"cases {cases}")
    print(f"nodes {total_nodes}")
    print(f"univalue {total_uni}")
    print(f"all-univalue trees {all_uni_trees}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    main()
