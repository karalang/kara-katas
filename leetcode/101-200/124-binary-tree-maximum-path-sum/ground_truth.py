"""Independent ground-truth check for #124.

Confirms the O(n) clamp-DP (max_path_sum in max_path_sum.py) equals a BRUTE-FORCE
maximum over every valid path, on many random small trees. A "path" in this
problem is any simple path in the (undirected) tree — equivalently, for a rooted
binary tree, every path is characterised by its TOP node: it goes down at most one
edge on each side. Brute force enumerates, for every node as the top, the best
downward chain on each side and takes val + best_left_down(≥0) + best_right_down(≥0),
then maxes over all tops. Independent of the DP's single-pass accumulation.
"""

import random

from max_path_sum import TreeNode, max_path_sum


def best_down(node):
    """Max sum of a downward chain starting at `node` (must include node)."""
    if node is None:
        return None  # no chain
    best = node.val
    for child in (node.left, node.right):
        d = best_down(child)
        if d is not None and node.val + d > best:
            best = node.val + d
    return best


def brute_force(root):
    """Max over every node-as-top of val + max(0,left_down) + max(0,right_down)."""
    if root is None:
        return None
    ld = best_down(root.left)
    rd = best_down(root.right)
    here = root.val + (ld if ld is not None and ld > 0 else 0) + (
        rd if rd is not None and rd > 0 else 0
    )
    best = here
    for child in (root.left, root.right):
        b = brute_force(child)
        if b is not None and b > best:
            best = b
    return best


def random_tree(n, rng):
    """A random binary tree of exactly n nodes, values in [-20, 20]."""
    if n == 0:
        return None
    val = rng.randint(-20, 20)
    left_n = rng.randint(0, n - 1)
    right_n = n - 1 - left_n
    return TreeNode(val, random_tree(left_n, rng), random_tree(right_n, rng))


def main():
    rng = random.Random(20260718)
    trials = 20000
    mismatches = 0
    for _ in range(trials):
        n = rng.randint(1, 12)
        root = random_tree(n, rng)
        dp = max_path_sum(root)
        bf = brute_force(root)
        if dp != bf:
            mismatches += 1
            if mismatches <= 5:
                print(f"MISMATCH n={n}: dp={dp} brute={bf}")
    if mismatches == 0:
        print(f"OK: clamp-DP == brute force on all {trials} random trees")
    else:
        print(f"FAIL: {mismatches}/{trials} mismatches")


if __name__ == "__main__":
    main()
