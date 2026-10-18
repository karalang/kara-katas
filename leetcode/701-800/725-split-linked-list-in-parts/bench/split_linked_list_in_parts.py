# LeetCode #725: Split Linked List in Parts -- count, then cut in place.
# Benchmark mirror of the Kara star arm: count the nodes, then walk the
# list once, taking each part's head, stepping to its last node and
# cutting the link after it.


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def split_list_to_parts(head, k):
    n = 0
    cur = head
    while cur is not None:
        n += 1
        cur = cur.next
    size, extra = n // k, n % k
    parts = []
    cur = head
    for i in range(k):
        parts.append(cur)
        length = size + 1 if i < extra else size
        if length > 0 and cur is not None:
            tail = cur
            for _ in range(length - 1):
                if tail.next is not None:
                    tail = tail.next
            cur = tail.next
            tail.next = None
    return parts


# Put the parts back together, starting from part `start` and going round.
def rejoin(parts, start):
    k = len(parts)
    head = None
    for i in range(k - 1, -1, -1):
        first = parts[(start + i) % k]
        if first is not None:
            tail = first
            while tail.next is not None:
                tail = tail.next
            tail.next = head
            head = first
    return head


def main():
    seed = [725]
    lists = []
    for _ in range(20):
        head = None
        for _ in range(1000):
            head = ListNode(next_random(seed) % 1000, head)
        lists.append(head)
    h = 0
    for rnd in range(5000):
        for d in range(20):
            k = 1 + (rnd * 7 + d) % 50
            parts = split_list_to_parts(lists[d], k)
            for p in parts:
                v = p.val + 1 if p is not None else 0
                h = (h * 31 + v) % 1000000007
            lists[d] = rejoin(parts, rnd % k)
    print(f"5000 rounds of 20 lists of 1000 numbers: hash {h}")


main()
