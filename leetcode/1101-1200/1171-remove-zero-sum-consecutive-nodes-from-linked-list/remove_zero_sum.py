# LeetCode #1171: Remove Zero Sum Consecutive Nodes from Linked List -- the
# mirror of the Kāra ★ arm, prefix sums in two passes. With `lit` as its
# argument it reads the statement literally instead: delete a run of
# consecutive values that sums to 0, the leftmost first, until none is left.
import sys


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def remove_zero_sum_sublists(head):
    dummy = ListNode(0, head)
    last = {}
    total = 0
    cur = dummy
    while cur:
        total += cur.val
        last[total] = cur
        cur = cur.next
    total = 0
    cur = dummy
    while cur:
        total += cur.val
        cur.next = last[total].next
        cur = cur.next
    return dummy.next


def literal(values):
    a = list(values)
    found = True
    while found:
        found = False
        for i in range(len(a)):
            s = 0
            for j in range(i, len(a)):
                s += a[j]
                if s == 0:
                    del a[i:j + 1]
                    found = True
                    break
            if found:
                break
    return a


def from_vec(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_vec(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(xs):
    h = 0
    for x in xs:
        h = (h * 131 + x + 1001) % 1000000007
    return h


def main():
    global seed
    if sys.argv[1:] == ['lit']:
        removed = literal
    else:
        def removed(values):
            return to_vec(remove_zero_sum_sublists(from_vec(values)))

    def show(values):
        print(f"[{', '.join(map(str, values))}] -> [{', '.join(map(str, removed(values)))}]")

    show([1, 2, -3, 3, 1])
    show([1, 2, 3, -3, 4])
    show([1, 2, 3, -3, -2])
    show([0])
    show([5, 7, -1])
    show([4, -4, 2, -2])
    show([1, -1, 1])
    show([2, 0, 3, -3, 1, -1, 0, 2])
    seed = 1171
    kept = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 30
        values = [next_random() % 7 - 3 for _ in range(n)]
        got = removed(values)
        kept += len(got)
        check = (check * 31 + digest(got)) % 1000000007
    print(f"300 random lists: {kept} kept, checksum {check}")
    for spread in [1000, 5]:
        values = [next_random() % (2 * spread + 1) - spread for _ in range(1000)]
        got = removed(values)
        print(f"1000 values within {spread}: {len(got)} kept, checksum {digest(got)}")
    values = [1] * 500 + [-1] * 499 + [2]
    got = removed(values)
    print(f"up 500 and down 499, then 2: [{', '.join(map(str, got))}]")


if __name__ == '__main__':
    main()
