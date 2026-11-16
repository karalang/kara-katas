# LeetCode #1172: Dinner Plate Stacks -- the mirror of the Kāra ★ arm: the
# stacks in a list and a heap of the indices that may have room, an index
# whose stack is full or gone dropped when it comes to the top. With `lit`
# as its argument it reads the statement literally instead: a push scans
# from the left for the first stack below capacity, `pop` scans from the
# right for the first stack with a plate, and no stack is ever dropped.
import heapq
import sys


class DinnerPlates:
    def __init__(self, capacity):
        self.capacity = capacity
        self.stacks = []
        self.open = []

    def push(self, val):
        while self.open:
            i = self.open[0]
            if i < len(self.stacks) and len(self.stacks[i]) < self.capacity:
                break
            heapq.heappop(self.open)
        if not self.open:
            heapq.heappush(self.open, len(self.stacks))
            self.stacks.append([])
        i = self.open[0]
        self.stacks[i].append(val)
        if len(self.stacks[i]) == self.capacity:
            heapq.heappop(self.open)

    def pop(self):
        if not self.stacks:
            return -1
        return self.pop_at_stack(len(self.stacks) - 1)

    def pop_at_stack(self, index):
        if index >= len(self.stacks) or not self.stacks[index]:
            return -1
        val = self.stacks[index].pop()
        heapq.heappush(self.open, index)
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        return val


class Literal:
    def __init__(self, capacity):
        self.capacity = capacity
        self.stacks = []

    def push(self, val):
        for s in self.stacks:
            if len(s) < self.capacity:
                s.append(val)
                return
        self.stacks.append([val])

    def pop(self):
        for s in reversed(self.stacks):
            if s:
                return s.pop()
        return -1

    def pop_at_stack(self, index):
        if index < len(self.stacks) and self.stacks[index]:
            return self.stacks[index].pop()
        return -1


LIT = len(sys.argv) > 1 and sys.argv[1] == "lit"


def run(capacity, ops):
    d = Literal(capacity) if LIT else DinnerPlates(capacity)
    out = []
    for kind, arg in ops:
        if kind == 0:
            d.push(arg)
        elif kind == 1:
            out.append(d.pop())
        else:
            out.append(d.pop_at_stack(arg))
    return out


seed = 1172


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(xs):
    h = 0
    for x in xs:
        h = (h * 131 + x + 2) % 1000000007
    return h


def random_ops(n, push, pop, at, spread):
    ops = []
    for _ in range(n):
        r = next_random() % (push + pop + at)
        if r < push:
            ops.append((0, 1 + next_random() % 20000))
        elif r < push + pop:
            ops.append((1, 0))
        else:
            ops.append((2, next_random() % spread))
    return ops


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    example = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (2, 0), (0, 20), (0, 21), (2, 0), (2, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]
    print(f"example, capacity 2: {show(run(2, example))}")
    print(f"empty: {show(run(3, [(1, 0), (2, 0), (2, 99999)]))}")
    print(f"past the last: {show(run(2, [(0, 7), (0, 8), (0, 9), (2, 2), (2, 1), (2, 5), (1, 0)]))}")
    print(f"capacity 1: {show(run(1, [(0, 1), (0, 2), (0, 3), (2, 1), (0, 4), (1, 0), (1, 0), (1, 0), (1, 0)]))}")
    print(f"holes refilled: {show(run(2, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (2, 0), (2, 1), (2, 0), (0, 7), (0, 8), (0, 9), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]))}")
    print(f"left emptied first: {show(run(2, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (2, 0), (2, 0), (2, 1), (2, 1), (1, 0), (1, 0), (0, 6), (2, 0), (1, 0)]))}")
    pops = 0
    check = 0
    for _ in range(300):
        capacity = 1 + next_random() % 4
        n = 1 + next_random() % 60
        ops = random_ops(n, 5, 2, 3, 12)
        got = run(capacity, ops)
        pops += len(got)
        check = (check * 31 + digest(got)) % 1000000007
    print(f"300 random streams: {pops} pops, checksum {check}")
    for capacity, n in [(1, 50000), (7, 200000), (20000, 200000)]:
        ops = random_ops(n, 6, 2, 2, 100000)
        got = run(capacity, ops)
        misses = sum(1 for x in got if x == -1)
        print(f"{n} calls, capacity {capacity}: {len(got)} pops, {misses} empty, checksum {digest(got)}")


main()
