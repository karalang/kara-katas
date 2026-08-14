"""LeetCode 270 — Closest BST Value (Python mirror / oracle).

Mirrors closest_bst_value.kara algorithm-for-algorithm: descend toward the
target, tracking the best candidate at every step, with the tie broken on VALUE
so the answer does not depend on visit order.
"""


def closest(val, left, right, root, target):
    best = val[root]
    best_diff = abs(val[root] - target)
    cur = root
    while cur >= 0:
        v = val[cur]
        d = abs(v - target)
        if d < best_diff or (d == best_diff and v < best):
            best = v
            best_diff = d
        cur = right[cur] if v < target else left[cur]
    return best


def fmt(x):
    """Match kāra's f-string rendering of an f64: integral values print bare."""
    return str(int(x)) if x == int(x) else repr(x)


def report(label, val, left, right, root, target):
    print(f"{label} target={fmt(target)} -> {closest(val, left, right, root, target)}")


def main():
    val = [4, 2, 5, 1, 3]
    left = [1, 3, -1, -1, -1]
    right = [2, 4, -1, -1, -1]
    for t in (3.714286, 0.5, 100.0, 2.5, 4.5, 1.5, 3.4, 3.6, 2.0, 5.0):
        report("[4,2,5,1,3]", val, left, right, 0, t)

    report("[7]", [7], [-1], [-1], 0, -3.25)

    v3, l3, r3 = [1, 10, 100], [-1, -1, -1], [1, 2, -1]
    report("[1,10,100] spine", v3, l3, r3, 0, 6.0)
    report("[1,10,100] spine", v3, l3, r3, 0, 5.5)


main()
