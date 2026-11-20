# LeetCode #1721: Swapping Nodes in a Linked List -- the bench
# (swap.kara): the kth node found, then a runner from it to the last node
# drags a second cursor from the head to the kth node from the end.


class ListNode:
    __slots__ = ("val", "next")

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


seed = 1721


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def main():
    count = 10
    rounds = 100
    n = 100000
    lists = []
    for _ in range(count):
        values = [next_random() % 101 for _ in range(n)]
        lists.append(build(values))
    ks = [wide() % n + 1 for _ in range(count * rounds)]
    total = 0
    check = 0
    for r in range(rounds):
        for c in range(count):
            head = swap_nodes(lists[c], ks[r * count + c])
            total += head.val
            check = (check * 31 + head.val + r) % 1000000007
    print(f"{count} lists of {n} nodes, {rounds} rounds: heads sum to {total}, checksum {check}")


main()
