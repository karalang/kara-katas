# LeetCode #2336: Smallest Number in Infinite Set -- the bench, the ★ arm
# in Python: every number from `next` on still in the set, and the
# numbers below it that were added back kept, as Python has no ordered
# set, in a `heapq` heap with a `set` beside it for membership.
import heapq


class SmallestInfiniteSet:
    def __init__(self):
        self.next = 1
        self.heap = []
        self.members = set()

    def pop_smallest(self):
        if self.heap:
            least = heapq.heappop(self.heap)
            self.members.discard(least)
            return least
        self.next += 1
        return self.next - 1

    def add_back(self, num):
        if num < self.next and num not in self.members:
            self.members.add(num)
            heapq.heappush(self.heap, num)


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    ops = []
    for i in range(200000):
        r = scrambled(i)
        ops.append(r // 3 % 5000 + 1 if r % 3 == 0 else 0)
    check = 0
    for _ in range(50):
        s = SmallestInfiniteSet()
        for op in ops:
            if op == 0:
                check = (check * 31 + s.pop_smallest()) % 1000000007
            else:
                s.add_back(op)
    print(f"50 passes over 2*10^5 calls: checksum {check}")


main()
