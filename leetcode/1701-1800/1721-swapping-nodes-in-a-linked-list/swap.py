# LeetCode #1721: Swapping Nodes in a Linked List -- mirrors swap.kara,
# the ★ arm: the kth node found, then a second cursor started from the
# head as a runner goes on from the kth node to the last; the second
# stops at the kth from the end, and the two values swap.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def swap_nodes(head, k):
    first = head
    for _ in range(k - 1):
        first = first.next
    second = head
    runner = first
    while runner.next is not None:
        runner = runner.next
        second = second.next
    first.val, second.val = second.val, first.val
    return head


seed = 0


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


def show(values):
    return "[" + ",".join(str(v) for v in values) + "]"


def swapped(values, k):
    return values_of(swap_nodes(build(values), k))


def batch(count, longest):
    nodes = 0
    check = 0
    for _ in range(count):
        n = next_random() % longest + 1
        k = next_random() % n + 1
        values = [next_random() % 101 for _ in range(n)]
        got = swapped(values, k)
        nodes += len(got)
        for v in got:
            check = (check * 31 + v + 1) % 1000000007
    print(f"{count} lists of up to {longest} nodes: {nodes} nodes, checksum {check}")


def main():
    global seed
    # LeetCode's two examples, then one node, two nodes, and the middle
    # node of an odd list swapped with itself
    print(show(swapped([1, 2, 3, 4, 5], 2)))
    print(show(swapped([7, 9, 6, 6, 7, 8, 3, 0, 9, 5], 5)))
    print(show(swapped([1], 1)))
    print(show(swapped([1, 2], 1)))
    print(show(swapped([1, 2, 3], 2)))
    seed = 1721
    batch(3000, 12)
    batch(300, 1000)
    batch(10, 100000)


main()
