"""LeetCode 148 — Sort List (Python mirror / oracle).

Top-down merge sort over a singly linked list. The Kāra version models nodes as
Vec-owned with a `weak` next overlay and rewires the weak links in place; here we
mirror the same algorithm on index links (`next_of[i]`) so the emitted order is
identical.
"""


def sort_list(vals):
    n = len(vals)
    next_of = [-1] * n
    for i in range(n - 1):
        next_of[i] = i + 1

    def split_mid(head):
        slow = head
        fast = next_of[head]
        while fast != -1:
            fast = next_of[fast]
            if fast != -1:
                slow = next_of[slow]
                fast = next_of[fast]
        mid = next_of[slow]
        next_of[slow] = -1
        return mid

    def merge(a, b):
        head = tail = -1
        while a != -1 and b != -1:
            if vals[a] <= vals[b]:
                pick, a = a, next_of[a]
            else:
                pick, b = b, next_of[b]
            if head == -1:
                head = pick
            else:
                next_of[tail] = pick
            tail = pick
        rest = a if a != -1 else b
        if tail != -1:
            next_of[tail] = rest
        return head

    def sort_chain(head):
        if head == -1 or next_of[head] == -1:
            return head
        mid = split_mid(head)
        left = sort_chain(head)
        right = sort_chain(mid)
        return merge(left, right)

    out = []
    if n == 0:
        return out
    cur = sort_chain(0)
    while cur != -1:
        out.append(vals[cur])
        cur = next_of[cur]
    return out


def run(vals):
    print(" ".join(str(x) for x in sort_list(vals)))


def main():
    run([4, 2, 1, 3])
    run([-1, 5, 3, 4, 0])
    run([])
    run([1])
    run([3, 3, 1, 2, 2])
    run([5, 4, 3, 2, 1])


main()
