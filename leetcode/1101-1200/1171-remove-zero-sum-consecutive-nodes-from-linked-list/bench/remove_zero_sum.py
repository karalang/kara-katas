# LeetCode #1171: Remove Zero Sum Consecutive Nodes from Linked List -- the
# ★ arm's bench in Python: prefix sums in two passes, the last node of each
# running sum kept in a dict. The same 32 lists and 400 rounds.


class ListNode:
    __slots__ = ("val", "next")

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


seed = 1171


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value(kind):
    if kind == 0:
        return next_random() % 5 - 2
    if kind == 1:
        return next_random() % 11 - 5
    if kind == 2:
        return next_random() % 101 - 50
    size = 1 + next_random() % 3
    return size if next_random() % 2 == 0 else -size


def main():
    rounds = 400
    lists = [[random_value(l % 4) for _ in range(1000)] for l in range(32)]
    kept = 0
    check = 0
    for _ in range(rounds):
        for l in range(32):
            i = next_random() % 1000
            lists[l][i] = random_value(l % 4)
            head = None
            for v in reversed(lists[l]):
                head = ListNode(v, head)
            cur = remove_zero_sum_sublists(head)
            while cur:
                kept += 1
                check = (check * 131 + cur.val + 1001) % 1000000007
                cur = cur.next
    print(f"{rounds} rounds over 32 lists of 1000 values: {kept} kept, checksum {check}")


main()
