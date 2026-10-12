# Benchmark for #430: mirror of flatten.kara (recursion). The walk
# breaks every link, as the Kāra program does, so reference counting
# frees the nodes without the cycle collector.
import sys


class Node:
    __slots__ = ("val", "prev", "next", "child")

    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None
        self.child = None


def flatten_level(head):
    cur = head
    while True:
        after = cur.next
        if cur.child is not None:
            c = cur.child
            child_tail = flatten_level(c)
            cur.next = c
            c.prev = cur
            cur.child = None
            if after is not None:
                child_tail.next = after
                after.prev = child_tail
            else:
                return child_tail
        if after is not None:
            cur = after
        else:
            return cur


def flatten(head):
    if head is not None:
        flatten_level(head)
    return head


seed = 430


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def make_level(length, budget, depth, next_val):
    head = None
    last = None
    for _ in range(length):
        if budget[0] == 0:
            break
        budget[0] -= 1
        node = Node(next_val[0])
        next_val[0] += 1
        if depth < 6 and budget[0] > 0 and step() % 4 == 0:
            child_length = 1 + step() % 8
            node.child = make_level(child_length, budget, depth + 1, next_val)
        if last is not None:
            last.next = node
            node.prev = last
        else:
            head = node
        last = node
    return head


def main():
    n = 1000
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    misplaced = 0
    checksum = 0
    for _ in range(rounds):
        budget = [n]
        next_val = [1]
        cur = flatten(make_level(n, budget, 0, next_val))
        expect = 1
        while cur is not None:
            if cur.val != expect:
                misplaced += 1
            expect += 1
            checksum = (checksum * 31 + cur.val) % 1000000007
            nxt = cur.next
            cur.prev = None
            cur.next = None
            cur = nxt
    print(f"{rounds} rounds of {n} nodes: {misplaced} misplaced, checksum {checksum}")


main()
