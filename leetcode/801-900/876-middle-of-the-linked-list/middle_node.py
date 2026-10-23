# LeetCode #876: Middle of the Linked List -- Python mirror of the ★ arm
# (slow and fast pointers) and its test harness; prints the same output
# as middle_node.kara.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def middle_node(head):
    slow = head
    fast = head
    while fast is not None:
        after = fast.next
        if after is None:
            break
        fast = after.next
        if slow is not None:
            slow = slow.next
    return slow


# ---- test harness ----------------------------------------------------------

seed = 876


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_values(head):
    values = []
    cur = head
    while cur is not None:
        values.append(cur.val)
        cur = cur.next
    return values


def text(values):
    if len(values) > 8:
        return f"[{values[0]}, {values[1]}, ... ({len(values)} nodes)]"
    return "[" + ", ".join(str(v) for v in values) + "]"


def show(values):
    answer = to_values(middle_node(from_values(values)))
    print(f"head = {text(values)} -> {text(answer)}")


def main():
    show([1, 2, 3, 4, 5])
    show([1, 2, 3, 4, 5, 6])
    show([1])
    show([1, 2])
    show([1, 2, 3])
    show([7, 7, 7, 7])
    show([100, 1, 100, 1, 100, 1, 100])
    show(list(range(1, 101)))
    show([100] * 99)
    values_sum = 0
    nodes_sum = 0
    check = 0
    for k in range(3000):
        n = k + 1 if k < 100 else next_random() % 100 + 1
        values = [next_random() % 100 + 1 for _ in range(n)]
        rest = to_values(middle_node(from_values(values)))
        values_sum += rest[0]
        nodes_sum += len(rest)
        check = (check * 131 + rest[0] * 101 + len(rest)) % 1000000007
    print(f"3000 lists of 1 to 100 nodes: middle values sum to {values_sum}, {nodes_sum} nodes from the middle on, checksum {check}")


main()
