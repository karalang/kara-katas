# LeetCode #2095: Delete the Middle Node of a Linked List -- Python mirror
# of the ★ arm (middle.kara): a slow and a fast runner, the slow one left
# just before the middle and stepping over it.


class ListNode:
    def __init__(self, val, next=None):
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


# ---- test harness -----------------------------------------------------------

seed = 2095


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
        [1, 3, 4, 7, 1, 2, 6],
        [1, 2, 3, 4],
        [2, 1],
        [5],
        [1, 2, 3],
        [9, 9, 9, 9, 9],
        [10, 20, 30, 40, 50, 60],
    ]
    for values in examples:
        print(f"{show(values)} -> {show(values_of(delete_middle(build(values))))}")
    check = 0
    kept = 0
    for _ in range(2000):
        n = next_random() % 200 + 1
        values = []
        for _ in range(n):
            hi = next_random()
            values.append((hi * 32768 + next_random()) % 100000 + 1)
        out = values_of(delete_middle(build(values)))
        kept += len(out)
        check = (check * 31 + checksum(out) + 1) % 1000000007
    print(f"2000 lists: {kept} values kept, checksum {check}")
    for n in [100000, 99999]:
        values = list(range(1, n + 1))
        out = values_of(delete_middle(build(values)))
        print(f"1 to {n}: {len(out)} kept, checksum {checksum(out)}, {out[n // 2 - 1]} then {out[n // 2]}")


main()
