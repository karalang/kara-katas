# LeetCode #2130: Maximum Twin Sum of a Linked List -- the mirror of
# twins.kara: the values read out, each in the first half with its twin.


class ListNode:
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def show(values):
    print(f"[{', '.join(map(str, values))}] -> {pair_sum(build(values))}")


def main():
    show([5, 4, 2, 1])
    show([4, 2, 2, 3])
    show([1, 100000])
    show([7, 7])
    show([1, 2, 9, 9, 2, 1])
    show([9, 1, 2, 3, 4, 9])
    show([3, 5, 1, 2, 4, 6])
    seed = [2130]
    total = 0
    check = 0
    for _ in range(2000):
        n = 2 * (next_random(seed) % 10 + 1)
        values = [next_random(seed) % 100 + 1 for _ in range(n)]
        s = pair_sum(build(values))
        total += s
        check = (check * 31 + s) % 1000000007
    print(f"2000 lists: {total} in all, checksum {check}")
    ladder = list(range(1, 100001))
    rand = []
    for _ in range(100000):
        hi = next_random(seed)
        rand.append((hi * 32768 + next_random(seed)) % 100000 + 1)
    a = pair_sum(build(ladder))
    b = pair_sum(build(rand))
    print(f"100000 nodes: {a} in order, {b} at random")


main()
