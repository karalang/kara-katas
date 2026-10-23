# LeetCode #876 bench: Python mirror of middle_node.kara (the ★ arm, slow
# and fast pointers) on the same 2,000,000 searches.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def middle_node(head):
    slow = head
    fast = head
    while fast is not None:
        after = fast.next
        if after is None:
            break
        fast = after.next
        if slow is not None:
            slow = slow.next
    return slow


seed = 876


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def main():
    lists = []
    for _ in range(2000):
        n = next_random() % 100 + 1
        lists.append(from_values([next_random() % 100 + 1 for _ in range(n)]))
    total = 0
    check = 0
    for k in range(2000000):
        middle = middle_node(lists[(k * 7 + k // 2000) % 2000])
        if middle is not None:
            total += middle.val
            check = (check * 131 + middle.val) % 1000000007
    print(f"2000000 searches over 2000 lists: middle values sum to {total}, checksum {check}")


main()
