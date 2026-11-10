# LeetCode #2058: Find the Minimum and Maximum Number of Nodes Between
# Critical Points -- Python mirror of the ★ arm (critical.kara): one walk
# with the value before each node, the first and last critical places and
# the smallest gap between neighbouring ones.


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


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def draw(n, top):
    return [next_random() % top + 1 for _ in range(n)]


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        [3, 1],
        [5, 3, 1, 2, 5, 1, 2],
        [1, 3, 2, 2, 3, 2, 2, 2, 7],
        [2, 3, 3, 2],
        [1, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 1, 1, 1],
        [4, 1, 9, 9, 9, 1, 4, 4, 8, 2],
    ]
    for values in examples:
        print(f"{show(values)} -> {show(nodes_between_critical_points(build(values)))}")
    found = total = check = 0
    for _ in range(2000):
        n = next_random() % 39 + 2
        top = next_random() % 9 + 2
        d = nodes_between_critical_points(build(draw(n, top)))
        if d[0] >= 0:
            found += 1
        total += d[0] + d[1]
        check = (check * 31 + d[0] + 2) % 1000000007
        check = (check * 31 + d[1] + 2) % 1000000007
    print(f"2000 short lists: {found} with two critical points, sum {total}, checksum {check}")
    found = total = check = 0
    for r in range(4):
        d = nodes_between_critical_points(build(draw(2000, [100000, 3, 2, 1][r])))
        if d[0] >= 0:
            found += 1
        total += d[0] + d[1]
        check = (check * 31 + d[0] + 2) % 1000000007
        check = (check * 31 + d[1] + 2) % 1000000007
    print(f"4 long lists: {found} with two critical points, sum {total}, checksum {check}")


main()
