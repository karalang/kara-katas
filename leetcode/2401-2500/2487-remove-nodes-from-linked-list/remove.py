# LeetCode #2487: Remove Nodes From Linked List -- Python mirror of the ★
# arm (remove.kara): a stack of the nodes kept so far, each new node
# popping the smaller ones, then the stack relinked in order.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def remove_nodes(head):
    stack = []
    cur = head
    while cur is not None:
        node = cur
        cur = node.next
        while stack and stack[-1].val < node.val:
            stack.pop()
        stack.append(node)
    result = None
    while stack:
        node = stack.pop()
        node.next = result
        result = node
    return result


# ---- test harness -----------------------------------------------------------

seed = 2487


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def values_of(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def checksum(v):
    check = 0
    for x in v:
        check = (check * 31 + x) % 1000000007
    return check


def main():
    examples = [
        [5, 2, 13, 3, 8],
        [1, 1, 1, 1],
        [7],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 3, 2, 3],
        [2, 9, 4, 9, 1, 1],
        [4, 6, 2, 6, 5, 3, 5],
    ]
    for values in examples:
        print(f"{show(values)} -> {show(values_of(remove_nodes(build(values))))}")
    for top in [100000, 5]:
        check = 0
        kept = 0
        for _ in range(2000):
            n = next_random() % 200 + 1
            values = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(n)]
            out = values_of(remove_nodes(build(values)))
            kept += len(out)
            check = (check * 31 + checksum(out) + 1) % 1000000007
        print(f"2000 lists of values to {top}: {kept} values kept, checksum {check}")
    falling = [100000 - i for i in range(100000)]
    rising = [i + 1 for i in range(100000)]
    same = [100000] * 100000
    random = [(next_random() * 32768 + next_random()) % 100000 + 1 for _ in range(100000)]
    for name, values in [("falling", falling), ("rising", rising), ("the same", same), ("random", random)]:
        out = values_of(remove_nodes(build(values)))
        print(f"10^5 {name}: {len(out)} kept, checksum {checksum(out)}")


main()
