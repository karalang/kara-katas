# LeetCode #1265 bench, in Python: the ★ arm (by recursion: a node prints
# after everything after it has) on 100 random lists of 1000 nodes built
# once, 300 rounds; everything each round prints folded into a checksum.
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


def main():
    seed = 1265
    printed = []
    heads = []
    for _ in range(100):
        head = None
        for _ in range(1000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            head = Node(seed // 65536 % 2001 - 1000, head, printed)
        heads.append(head)
    check = 0
    for rnd in range(300):
        for h in heads:
            printed.clear()
            print_linked_list_in_reverse(h)
            check = (check + rnd) % 1000000007
            for v in printed:
                check = (check * 131 + v + 1000) % 1000000007
    print(f"300 rounds of 100 lists of 1000 nodes: checksum {check}")


main()
