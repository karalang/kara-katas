# LeetCode #2046: Sort Linked List Already Sorted Using Absolute Values --
# Python mirror of the ★ arm (sort.kara): one walk moves every negative node
# after the head to the front. Output is byte-identical to the Kāra arms.


class ListNode:
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


def draw(n, top):
    values = [next_random() % (2 * top + 1) - top for _ in range(n)]
    return sorted(values, key=abs)


def fold_in(check, values):
    for v in values:
        check = (check * 31 + v + 5001) % 1000000007
    return check


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        [0, 2, -5, 5, 10, -10],
        [0, 1, 2],
        [1],
        [-1],
        [-1, -2, -3, -4],
        [1, -1, 2, -2, 3, -3],
        [0, 0, -3, 3, -3, 5000, -5000],
        [-7, 8, -9],
    ]
    for values in examples:
        print(f"{show(values)} -> {show(values_of(sort_linked_list(build(values))))}")
    seed = 2046
    negatives = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 20 + 1
        top = next_random() % 30 + 1
        s = values_of(sort_linked_list(build(draw(n, top))))
        negatives += sum(1 for v in s if v < 0)
        check = fold_in(check, s)
    print(f"2000 short lists: {negatives} negatives, checksum {check}")
    negatives = 0
    check = 0
    for r in range(4):
        values = draw(100000, [5000, 100, 1, 5000][r])
        if r == 3:
            values = [-abs(v) for v in values]
        s = values_of(sort_linked_list(build(values)))
        negatives += sum(1 for v in s if v < 0)
        check = fold_in(check, s)
    print(f"4 long lists: {negatives} negatives, checksum {check}")


main()
