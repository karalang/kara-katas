# LeetCode #2058: Find the Minimum and Maximum Number of Nodes Between
# Critical Points -- Python mirror of the ★ arm's benchmark (critical.kara):
# the same 50 lists of 100000 values, each built node by node and answered
# by one walk.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def nodes_between_critical_points(head):
    if head is None:
        return [-1, -1]
    before = head.val
    cur = head.next
    at = 1
    first = last = nearest = -1
    while cur is not None:
        after = cur.next
        if after is not None:
            v = cur.val
            if (v > before and v > after.val) or (v < before and v < after.val):
                if first < 0:
                    first = at
                elif nearest < 0 or at - last < nearest:
                    nearest = at - last
                last = at
        before = cur.val
        cur = cur.next
        at += 1
    return [-1, -1] if nearest < 0 else [nearest, last - first]


seed = 2058


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    tops = [2, 3, 10, 100000]
    total = check = 0
    for t in range(50):
        top = tops[t % 4]
        head = None
        for _ in range(100000):
            head = ListNode(next_random() % top + 1, head)
        d = nodes_between_critical_points(head)
        total += d[0] + d[1]
        check = (check * 31 + d[0] + 2) % 1000000007
        check = (check * 31 + d[1] + 2) % 1000000007
    print(f"50 lists: sum {total}, checksum {check}")


main()
