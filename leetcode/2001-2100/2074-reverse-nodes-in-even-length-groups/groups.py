# LeetCode #2074: Reverse Nodes in Even Length Groups -- Python mirror of
# the ★ arm (groups.kara): one walk a group at a time, each group counted
# up to the length it should have and turned round in place when the
# count is even.


class ListNode:
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


seed = 2074


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
        [5, 2, 6, 3, 9, 1, 7, 3, 8, 4],
        [1, 1, 0, 6],
        [1, 1, 0, 6, 5],
        [7],
        [1, 2],
        list(range(1, 22)),
        list(range(1, 15)),
    ]
    for values in examples:
        print(f"{show(values)} -> {show(values_of(reverse_even_length_groups(build(values))))}")
    check = 0
    for _ in range(500):
        n = next_random() % 200 + 1
        values = [next_random() % 100001 for _ in range(n)]
        check = (check * 31 + checksum(values_of(reverse_even_length_groups(build(values))))) % 1000000007
    print(f"500 lists: checksum {check}")
    values = [next_random() % 100001 for _ in range(100000)]
    out = values_of(reverse_even_length_groups(build(values)))
    print(f"100000 values: checksum {checksum(out)}, first {out[0]}, last {out[-1]}")


main()
