"""LeetCode 147 — Insertion Sort List (Python mirror / oracle).

Insertion sort over a singly linked list: for each node, scan the sorted
prefix from the head to find the insertion point, then splice it in. The Kāra
version models nodes as Vec-owned with a `weak` next overlay and rewires the
weak links in place; here we mirror the same algorithm on index links so the
emitted order is identical.
"""


def sort_list(vals):
    n = len(vals)
    # next_of[i] = index of the node after i in the sorted chain, or -1.
    next_of = [-1] * n
    head = -1
    for i in range(n):
        v = vals[i]
        if head == -1:
            head = i
        elif vals[head] >= v:
            next_of[i] = head
            head = i
        else:
            prev = head
            while next_of[prev] != -1 and vals[next_of[prev]] < v:
                prev = next_of[prev]
            next_of[i] = next_of[prev]
            next_of[prev] = i

    out = []
    cur = head
    while cur != -1:
        out.append(vals[cur])
        cur = next_of[cur]
    return out


def run(vals):
    print(" ".join(str(x) for x in sort_list(vals)))


def main():
    run([4, 2, 1, 3])
    run([-1, 5, 3, 4, 0])
    run([1])
    run([3, 1, 2, 2, 1])
    run([5, 4, 3, 2, 1])


main()
