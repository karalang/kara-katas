# LeetCode #2046 -- the ★ arm as a benchmark; mirror of sort.kara.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def sort_linked_list(head):
    if head is None:
        return None
    front = head
    prev = head
    cur = head.next
    while cur is not None:
        node = cur
        cur = node.next
        if node.val < 0:
            prev.next = node.next
            node.next = front
            front = node
        else:
            prev = node
    return front


def build(m, rnd):
    head = None
    for j in range(m - 1, -1, -1):
        v = -(j // 2) if (7 * j + rnd) % 3 == 0 else j // 2
        head = ListNode(v, head)
    return head


def main():
    rounds, m = 20000, 1000
    negatives = 0
    check = 0
    for r in range(rounds):
        cur = sort_linked_list(build(m, r))
        while cur is not None:
            if cur.val < 0:
                negatives += 1
            check = (check * 31 + cur.val + 1000) % 1000000007
            cur = cur.next
    print(f"{rounds} rounds: {negatives} negatives, checksum {check}")


main()
