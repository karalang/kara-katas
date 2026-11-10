# LeetCode #2074: Reverse Nodes in Even Length Groups -- Python mirror of
# the ★ arm's benchmark (groups.kara): 2000 rounds, each a fresh list of
# 10000 values turned group by group in place and folded into a checksum.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def reverse_even_length_groups(head):
    if head is None:
        return None
    before = head
    want = 2
    while before.next is not None:
        start = before.next
        length = 0
        end = start
        cur = start
        while length < want and cur is not None:
            length += 1
            end = cur
            cur = cur.next
        if length % 2 == 0:
            turned = end.next
            rest = start
            for _ in range(length):
                node = rest
                rest = node.next
                node.next = turned
                turned = node
            before.next = turned
            before = start
        else:
            before = end
        want += 1
    return head


def build(m, rnd):
    head = None
    for j in range(m - 1, -1, -1):
        head = ListNode((j * 7919 + rnd) % 100001, head)
    return head


def main():
    check = 0
    for r in range(2000):
        cur = reverse_even_length_groups(build(10000 + r % 7, r))
        while cur is not None:
            check = (check * 31 + cur.val) % 1000000007
            cur = cur.next
    print(f"2000 rounds: checksum {check}")


main()
