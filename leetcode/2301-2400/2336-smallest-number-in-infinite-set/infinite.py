# LeetCode #2336: Smallest Number in Infinite Set -- the Python mirror of
# the ★ arm: every number from `next` on still in the set, and the
# numbers below it that were added back kept in a sorted list.
import bisect


class SmallestInfiniteSet:
    def __init__(self):
        self.next = 1
        self.returned = []

    def pop_smallest(self):
        if self.returned:
            return self.returned.pop(0)
        self.next += 1
        return self.next - 1

    def add_back(self, num):
        if num < self.next:
            at = bisect.bisect_left(self.returned, num)
            if at == len(self.returned) or self.returned[at] != num:
                self.returned.insert(at, num)


SEED = [2336]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def run(ops):
    s = SmallestInfiniteSet()
    popped = []
    for op in ops:
        if op == 0:
            popped.append(s.pop_smallest())
        else:
            s.add_back(op)
    return popped


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    print(show(run([2, 0, 0, 0, 1, 0, 0, 0])))
    print(show(run([0, 0, 0, 0, 0])))
    print(show(run([5, 0, 3, 0, 0, 2, 0, 0])))
    long = []
    for i in range(1000):
        long.append(0)
        if i % 10 == 9:
            long.append(i // 2 + 1)
    popped = run(long)
    print(f"1000 pops: last {popped[-1]}, sum {sum(popped)}")
    check = 0
    pops = 0
    for _ in range(2000):
        calls = next_random() % 40 + 1
        ops = []
        for _ in range(calls):
            if next_random() % 2 == 0:
                ops.append(0)
            else:
                ops.append(next_random() % 30 + 1)
        for value in run(ops):
            check = (check * 31 + value) % 1000000007
            pops += 1
    print(f"2000 sequences: checksum {check}, {pops} pops")


main()
