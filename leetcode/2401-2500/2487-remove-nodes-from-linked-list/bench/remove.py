# LeetCode #2487: Remove Nodes From Linked List -- Python mirror of the ★
# arm's benchmark (remove.kara): the same lists of 1000 nodes, each
# cleared by the same stack, the kept nodes folded into the checksum.


class ListNode:
    __slots__ = ("val", "next")

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


def build(m, round, check):
    head = None
    for j in range(m - 1, -1, -1):
        head = ListNode((m - j) * 10 + (round * 7919 + j * 104729 + check) % 37, head)
    return head


def main():
    rounds = 22000
    kept = 0
    check = 0
    for r in range(rounds):
        cur = remove_nodes(build(1000, r, check))
        while cur is not None:
            kept += 1
            check = (check * 31 + cur.val) % 1000000007
            cur = cur.next
    print(f"{rounds} lists of 1000 nodes: {kept} kept, checksum {check}")


main()
