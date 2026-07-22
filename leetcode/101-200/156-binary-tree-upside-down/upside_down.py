"""LeetCode 156 — Binary Tree Upside Down (Python mirror / oracle). Premium.

Iterative left-spine rewire: old left child becomes the new root, old parent
becomes its right child, old right sibling becomes its left child. Mirrors the
Kāra version on an index-linked node pool, serialized pre-order (# = null).
"""


def flip(left, right, root):
    cur, prev, prev_right = root, -1, -1
    while cur != -1:
        nxt = left[cur]
        left[cur] = prev_right
        prev_right = right[cur]
        right[cur] = prev
        prev, cur = cur, nxt
    return prev


def serialize(vals, left, right, root, out):
    if root == -1:
        out.append("#")
        return
    out.append(str(vals[root]))
    serialize(vals, left, right, left[root], out)
    serialize(vals, left, right, right[root], out)


def main():
    vals = [1, 2, 3, 4, 5]
    left = [1, 3, -1, -1, -1]
    right = [2, 4, -1, -1, -1]
    nr = flip(left, right, 0)
    out = []
    serialize(vals, left, right, nr, out)
    print(" ".join(out) + " ")

    vals2 = [7]
    left2 = [-1]
    right2 = [-1]
    sr = flip(left2, right2, 0)
    out2 = []
    serialize(vals2, left2, right2, sr, out2)
    print(" ".join(out2) + " ")


main()
