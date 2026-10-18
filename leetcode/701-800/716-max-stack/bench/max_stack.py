# LeetCode #716: Max Stack -- a stack of running maxima beside it.
# Benchmark mirror of the Kara star arm: each value with the largest
# value at or below it; pop_max pops into a buffer until the max is on
# top, drops it, and pushes the buffer back.


class MaxStack:
    def __init__(self):
        self.values = []
        self.maxes = []

    def push(self, x):
        m = x
        if self.maxes and self.maxes[-1] > x:
            m = self.maxes[-1]
        self.values.append(x)
        self.maxes.append(m)

    def pop(self):
        self.maxes.pop()
        return self.values.pop()

    def top(self):
        return self.values[-1]

    def peek_max(self):
        return self.maxes[-1]

    def pop_max(self):
        m = self.peek_max()
        buffer = []
        while self.top() != m:
            buffer.append(self.pop())
        self.pop()
        while buffer:
            self.push(buffer.pop())
        return m


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [716]
    lists = []
    for _ in range(10):
        calls = []
        size = 0
        for _ in range(100000):
            if size == 0 or next_random(seed) % 2 == 0:
                hi = next_random(seed)
                lo = next_random(seed)
                calls.append((0, (hi * 32768 + lo) % 1000001))
                size += 1
            else:
                kind = 1 + next_random(seed) % 4
                calls.append((kind, 0))
                if kind == 1 or kind == 4:
                    size -= 1
        lists.append(calls)
    total = 0
    for _ in range(10):
        for calls in lists:
            s = MaxStack()
            for kind, x in calls:
                if kind == 0:
                    s.push(x)
                elif kind == 1:
                    total += s.pop()
                elif kind == 2:
                    total += s.top()
                elif kind == 3:
                    total += s.peek_max()
                else:
                    total += s.pop_max()
    print(f"10 rounds of 10 lists of 100000 calls: sum {total}")


main()
