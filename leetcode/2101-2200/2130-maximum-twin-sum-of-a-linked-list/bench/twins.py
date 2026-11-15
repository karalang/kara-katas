# LeetCode #2130: Maximum Twin Sum of a Linked List -- the benchmark, the
# same algorithm as twins.kara.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def pair_sum(head):
    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next
    n = len(values)
    best = 0
    for i in range(n // 2):
        best = max(best, values[i] + values[n - 1 - i])
    return best


seed = 2130


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100000
    lists = []
    for _ in range(10):
        head = None
        for _ in range(n):
            hi = next_random()
            head = ListNode((hi * 32768 + next_random()) % 100000 + 1, head)
        lists.append(head)
    total = 0
    check = 0
    for rnd in range(50):
        for k in range(10):
            hi = next_random()
            at = (hi * 32768 + next_random()) % n
            node = lists[k]
            for _ in range(at):
                node = node.next
            node.val = next_random() % 200000 + 1
            s = pair_sum(lists[k])
            total += s
            check = (check * 31 + s + rnd) % 1000000007
    print(f"500 solves: {total} in all, checksum {check}")


main()
