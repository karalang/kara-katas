# Benchmark mirror of linked_list_random.kara (#382).


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class Solution:
    def __init__(self, head):
        self.head = head
        self.seed = 382

    def below(self, n):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return (self.seed // 65536) % n

    def get_random(self):
        kept = 0
        i = 0
        at = self.head
        while at is not None:
            i += 1
            if self.below(i) == 0:
                kept = at.val
            at = at.next
        return kept


def main():
    seed = 7
    head = None
    for _ in range(10000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        head = ListNode((seed // 65536) % 20001 - 10000, head)
    s = Solution(head)
    checksum = 0
    for _ in range(20000):
        checksum = (checksum * 31 + s.get_random() + 10000) % 1000000007
    print(f"checksum {checksum}")


main()
