# LeetCode #2095: Delete the Middle Node of a Linked List -- Python mirror
# of the ★ arm's benchmark (middle.kara): the same 20000 lists, each with its
# middle deleted 50 times by the same two runners.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next):
        self.val = val
        self.next = next


def delete_middle(head):
    if head is None or head.next is None:
        return None
    slow = head
    fast = head.next.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    slow.next = slow.next.next
    return head


def build(m, rnd):
    head = None
    for j in range(m - 1, -1, -1):
        head = ListNode((rnd * 7919 + j * 104729) % 100000 + 1, head)
    return head


def main():
    rounds = 20000
    left = 0
    check = 0
    for r in range(rounds):
        lst = build(1000, r)
        for _ in range(50):
            lst = delete_middle(lst)
        cur = lst
        while cur is not None:
            left += 1
            check = (check * 31 + cur.val) % 1000000007
            cur = cur.next
    print(f"{rounds} rounds: {left} nodes left, checksum {check}")


main()
