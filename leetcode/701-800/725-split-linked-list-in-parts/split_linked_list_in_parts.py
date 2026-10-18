# LeetCode #725: Split Linked List in Parts -- count, then cut in place.
# Mirror of the Kara star arm and its harness.


class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


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


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_values(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def split_values(values, k):
    return [to_values(p) for p in split_list_to_parts(from_values(values), k)]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(values, k):
    print(f"{values}, k = {k} -> {split_values(values, k)}")


def summary(values, k):
    parts = split_values(values, k)
    lengths = [len(p) for p in parts]
    joined = [v for p in parts for v in p]
    print(f"{len(values)} numbers, k = {k} -> lengths {lengths}, rejoined {'true' if joined == values else 'false'}")


def main():
    show([1, 2, 3], 5)
    show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
    show([], 3)
    show([7], 1)
    show([1, 2, 3, 4, 5, 6], 3)
    show([4, 0, 4], 1)
    show([5, 6, 7, 8], 4)
    show([1, 2, 3, 4, 5, 6, 7], 6)
    seed = [725]
    big = [next_random(seed) % 1001 for _ in range(1000)]
    summary(list(big), 7)
    summary(list(big), 1)
    big.pop()
    summary(list(big), 50)
    s = 0
    for _ in range(300):
        n = next_random(seed) % 21
        k = 1 + next_random(seed) % 8
        values = [next_random(seed) % 1001 for _ in range(n)]
        for p in split_values(values, k):
            s = (s * 131 + len(p) + 1) % 1000000007
            for v in p:
                s = (s * 131 + v) % 1000000007
    print(f"300 random lists: checksum {s}")


main()
