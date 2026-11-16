# LeetCode #1172: Dinner Plate Stacks -- the ★ arm's bench in Python: the
# stacks in a list and a heapq min-heap of the indices that may have room,
# an index whose stack is full or gone dropped when it comes to the top.
# The same 60 streams of 200000 calls.
import heapq


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


seed = 1172


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    streams = 60
    calls = 200000
    capacities = [1, 7, 100, 20000]
    pops = misses = check = 0
    for s in range(streams):
        capacity = capacities[s % 4]
        spread = 20000 // capacity + 1
        d = DinnerPlates(capacity)
        for _ in range(calls):
            r = next_random() % 10
            if r < 6:
                d.push(1 + next_random() % 20000)
                continue
            elif r < 8:
                got = d.pop()
            else:
                got = d.pop_at_stack(next_random() % spread)
            pops += 1
            if got == -1:
                misses += 1
            check = (check * 131 + got + 2) % 1000000007
    print(f"{streams} streams of {calls} calls: {pops} pops, {misses} empty, checksum {check}")


main()
