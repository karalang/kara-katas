# LeetCode #382: Linked List Random Node -- mirror of
# linked_list_random.kara (reservoir sampling).
import math


class ListNode:
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


def from_values(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def b(x):
    return "true" if x else "false"


def fair(values, draws):
    lo, hi = min(values), max(values)
    want = [0] * (hi - lo + 1)
    for v in values:
        want[v - lo] += 1
    got = [0] * (hi - lo + 1)
    s = Solution(from_values(values))
    for _ in range(draws):
        x = s.get_random()
        if x < lo or x > hi or want[x - lo] == 0:
            return False
        got[x - lo] += 1
    n = len(values)
    chi = 0.0
    kinds = 0
    for k in range(len(want)):
        if want[k] > 0:
            kinds += 1
            e = (draws * want[k]) / n
            d = got[k] - e
            chi += d * d / e
    dof = float(kinds - 1)
    return chi <= dof + 6.0 * math.sqrt(2.0 * dof) + 12.0


def main():
    print(f"example [1, 2, 3], 30000 draws: fair {b(fair([1, 2, 3], 30000))}")
    one = Solution(from_values([7]))
    always = all(one.get_random() == 7 for _ in range(100))
    print(f"one node: always 7 {b(always)}")
    print(f"duplicates [4, 4, 9]: fair {b(fair([4, 4, 9], 30000))}")
    print(f"negative values [-5, 0, 5, -5]: fair {b(fair([-5, 0, 5, -5], 30000))}")
    long = [i % 37 for i in range(1000)]
    print(f"1000 nodes of 37 values: fair {b(fair(long, 5000))}")
    seed = 382
    passed = 0
    nodes = 0
    for _ in range(200):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 60
        values = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            values.append((seed // 65536) % 40 - 20)
        nodes += n
        if fair(values, 20 * n):
            passed += 1
    print(f"200 random lists, {nodes} nodes: {passed} fair")


main()
