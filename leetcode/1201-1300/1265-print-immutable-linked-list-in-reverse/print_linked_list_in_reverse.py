# LeetCode #1265: Print Immutable Linked List in Reverse -- Python mirror of
# the ★ arm (by recursion: a node prints after everything after it has),
# with the same harness.
import sys

sys.setrecursionlimit(10000)


def print_linked_list_in_reverse(head):
    nxt = head.get_next()
    if nxt is not None:
        print_linked_list_in_reverse(nxt)
    head.print_value()


class Node:
    def __init__(self, val, nxt, printed):
        self.val = val
        self.next = nxt
        self.printed = printed

    def print_value(self):
        self.printed.append(self.val)

    def get_next(self):
        return self.next


def printed_in_reverse(values):
    printed = []
    head = None
    for v in reversed(values):
        head = Node(v, head, printed)
    print_linked_list_in_reverse(head)
    return printed


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    print(show(printed_in_reverse([1, 2, 3, 4])))
    print(show(printed_in_reverse([0, -4, -1, 3, -5])))
    print(show(printed_in_reverse([-2, 0, 6, 4, 4, -6])))
    rng = Rng(1265)
    total = check = 0
    for _ in range(1000):
        n = rng.next() % 60 + 1
        values = [rng.next() % 2001 - 1000 for _ in range(n)]
        got = printed_in_reverse(values)
        total += len(got)
        for v in got:
            check = (check * 131 + v + 1000) % 1000000007
    print(f"1000 random lists: {total} values printed, checksum {check}")
    got = printed_in_reverse([i * 7 % 2001 - 1000 for i in range(1000)])
    print(f"1000 nodes: first {got[0]}, last {got[999]}, {len(got)} printed")


main()
