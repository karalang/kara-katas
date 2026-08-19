#!/usr/bin/env python3
"""LeetCode 285 — differential harness. Mirror of differential.kara.

Two descents (iterative with a mutable best, recursive with a fallback) against
an inorder walk that makes no claim about the tree's shape.
"""


class Bst:
    def __init__(self):
        self.key, self.left, self.right = [], [], []


def bst_insert(t, k):
    if not t.key:
        t.key.append(k); t.left.append(-1); t.right.append(-1)
        return
    cur = 0
    while True:
        if k < t.key[cur]:
            if t.left[cur] < 0:
                t.key.append(k); t.left.append(-1); t.right.append(-1)
                t.left[cur] = len(t.key) - 1
                return
            cur = t.left[cur]
        else:
            if t.right[cur] < 0:
                t.key.append(k); t.left.append(-1); t.right.append(-1)
                t.right[cur] = len(t.key) - 1
                return
            cur = t.right[cur]


def build(keys):
    t = Bst()
    for k in keys:
        bst_insert(t, k)
    return t


def successor_iter(t, target):
    if not t.key:
        return None
    cur, best = 0, None
    while cur >= 0:
        if t.key[cur] > target:
            best = t.key[cur]
            cur = t.left[cur]
        else:
            cur = t.right[cur]
    return best


def successor_rec_from(t, node, target):
    if node < 0:
        return None
    if t.key[node] <= target:
        return successor_rec_from(t, t.right[node], target)
    inner = successor_rec_from(t, t.left[node], target)
    return inner if inner is not None else t.key[node]


def successor_rec(t, target):
    if not t.key:
        return None
    return successor_rec_from(t, 0, target)


def successor_in(t, target):
    if not t.key:
        return None
    stack, cur = [], 0
    while cur >= 0 or stack:
        while cur >= 0:
            stack.append(cur)
            cur = t.left[cur]
        node = stack.pop()
        if t.key[node] > target:
            return t.key[node]
        cur = t.right[node]
    return None


def main():
    cases = probes_run = none_answers = 0
    iter_vs_inorder = rec_vs_inorder = digest = deepest = 0

    seed = 20260824
    for shape in range(3):
        for n in range(1, 13):
            for _ in range(12):
                keys = []
                for i in range(n):
                    if shape == 0:
                        seed = (seed * 1103515245 + 12345) % 2147483648
                        keys.append((seed // 7) % 40)
                    elif shape == 1:
                        keys.append(i * 3)
                    else:
                        keys.append((n - i) * 3)
                t = build(keys)
                deepest = max(deepest, len(t.key))

                for p in range(len(keys)):
                    for d in (-1, 0, 1):
                        target = keys[p] + d
                        a = successor_iter(t, target)
                        b = successor_rec(t, target)
                        c = successor_in(t, target)
                        if a != c:
                            iter_vs_inorder += 1
                        if b != c:
                            rec_vs_inorder += 1
                        if c is None:
                            none_answers += 1
                        digest = (digest * 131 + (c if c is not None else -7) + 11) % 1000000007
                        probes_run += 1
                cases += 1

    print(f"trees {cases}, probes {probes_run}, deepest tree {deepest} nodes")
    print(f"probes with NO successor {none_answers}")
    print(f"digest {digest}")
    print(f"iterative vs the inorder definition {iter_vs_inorder}")
    print(f"recursive vs the inorder definition {rec_vs_inorder}")


main()
