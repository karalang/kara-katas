#!/usr/bin/env python3
"""LeetCode 272 — Closest Binary Search Tree Value II. Mirror of the ★ solver.

Same two-stack merge, same parallel-array tree, same tie rule (equal distance ->
the smaller value, which the predecessor always is).
"""


def advance_pred(val, left, right, pred):
    node = pred.pop()
    cur = left[node]
    while cur >= 0:
        pred.append(cur)
        cur = right[cur]
    return val[node]


def advance_succ(val, left, right, succ):
    node = succ.pop()
    cur = right[node]
    while cur >= 0:
        succ.append(cur)
        cur = left[cur]
    return val[node]


def closest_k(val, left, right, root, target, k):
    pred, succ = [], []
    cur = root
    while cur >= 0:
        if val[cur] < target:
            pred.append(cur)
            cur = right[cur]
        else:
            succ.append(cur)
            cur = left[cur]

    lower, upper = [], []
    taken = 0
    while taken < k:
        have_p, have_s = len(pred) > 0, len(succ) > 0
        if not have_p and not have_s:
            break
        take_pred = have_p
        if have_p and have_s:
            dp = abs(val[pred[-1]] - target)
            ds = abs(val[succ[-1]] - target)
            take_pred = dp <= ds  # tie -> the predecessor, the smaller value
        if take_pred:
            lower.append(advance_pred(val, left, right, pred))
        else:
            upper.append(advance_succ(val, left, right, succ))
        taken += 1

    return lower[::-1] + upper


def show(xs):
    return "[" + ",".join(str(x) for x in xs) + "]"


def main():
    val = [4, 2, 5, 1, 3]
    left = [1, 3, -1, -1, -1]
    right = [2, 4, -1, -1, -1]

    print(show(closest_k(val, left, right, 0, 3.714286, 2)))
    print(show(closest_k(val, left, right, 0, 3.714286, 4)))
    print(show(closest_k(val, left, right, 0, 2.5, 1)))
    print(show(closest_k(val, left, right, 0, 2.5, 3)))
    print(show(closest_k(val, left, right, 0, -10.0, 3)))
    print(show(closest_k(val, left, right, 0, 3.5, 9)))


main()
