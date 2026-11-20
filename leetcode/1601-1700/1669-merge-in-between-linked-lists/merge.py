# LeetCode #1669: Merge In Between Linked Lists -- the Python mirror of the
# ★ arm: the two ends of the cut found first.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def merge_in_between(list1, a, b, list2):
    before = list1
    for _ in range(1, a):
        before = before.next
    after = before.next
    for _ in range(a, b + 1):
        after = after.next
    last = list2
    while last.next is not None:
        last = last.next
    before.next = list2
    last.next = after
    return list1


# ---- the harness: the same as the Kāra arms -------------------------------

seed = 1669


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


def merged(list1, a, b, list2):
    return values_of(merge_in_between(build(list1), a, b, build(list2)))


def batch(count, longest):
    nodes = 0
    check = 0
    for _ in range(count):
        n = next_random() % (longest - 2) + 3
        m = next_random() % longest + 1
        a = next_random() % (n - 2) + 1
        b = a + next_random() % (n - 1 - a)
        list1 = [next_random() % 1000001 for _ in range(n)]
        list2 = [next_random() % 1000001 for _ in range(m)]
        got = merged(list1, a, b, list2)
        nodes += len(got)
        for v in got:
            check = (check * 31 + v + 1) % 1000000007
    print(f"{count} problems of up to {longest} nodes: {nodes} nodes merged, checksum {check}")


print(show(merged([10, 1, 13, 6, 9, 5], 3, 4, [1000000, 1000001, 1000002])))
print(show(merged([0, 1, 2, 3, 4, 5, 6], 2, 5, [1000000, 1000001, 1000002, 1000003, 1000004])))
print(show(merged([1, 2, 3], 1, 1, [9])))
print(show(merged([1, 2, 3, 4, 5], 1, 3, [7, 8])))
batch(3000, 12)
batch(300, 1000)
batch(10, 10000)
