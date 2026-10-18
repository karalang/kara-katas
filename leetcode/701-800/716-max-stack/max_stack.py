# LeetCode #716: Max Stack -- a stack of running maxima beside it.
#
# A mirror of max_stack.kara (the ★ arm) and its harness.


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


def run(calls):
    s = MaxStack()
    answers = []
    for kind, x in calls:
        if kind == 0:
            s.push(x)
        elif kind == 1:
            answers.append(s.pop())
        elif kind == 2:
            answers.append(s.top())
        elif kind == 3:
            answers.append(s.peek_max())
        else:
            answers.append(s.pop_max())
    return answers


def random_calls(seed, count, push_weight, spread):
    calls = []
    size = 0
    for _ in range(count):
        if size == 0 or next_random(seed) % 8 < push_weight:
            hi = next_random(seed)
            lo = next_random(seed)
            x = (hi * 32768 + lo) % (2 * spread + 1) - spread
            calls.append((0, x))
            size += 1
        else:
            kind = 1 + next_random(seed) % 4
            calls.append((kind, 0))
            if kind == 1 or kind == 4:
                size -= 1
    return calls


def summary(name, answers):
    total = 0
    for a in answers:
        total = (total * 131 + a + 10000001) % 1000000007
    print(f"{name}: {len(answers)} answers, checksum {total}")


def main():
    print(run([(0, 5), (0, 1), (0, 5), (2, 0), (4, 0), (2, 0), (3, 0), (1, 0), (2, 0)]))
    print(run([(0, 7), (3, 0), (2, 0), (4, 0), (0, -3), (3, 0), (1, 0)]))
    print(run([(0, 1), (0, 2), (0, 3), (0, 4), (4, 0), (4, 0), (3, 0), (2, 0), (4, 0), (4, 0)]))
    print(run([(0, 4), (0, 3), (0, 2), (0, 1), (4, 0), (2, 0), (3, 0), (4, 0), (3, 0), (1, 0), (3, 0)]))
    print(run([(0, 2), (0, 2), (0, 1), (0, 2), (4, 0), (2, 0), (4, 0), (2, 0), (3, 0), (4, 0), (3, 0)]))
    print(run([(0, -10000000), (0, 10000000), (0, -10000000), (3, 0), (4, 0), (3, 0), (2, 0), (0, 10000000), (0, 10000000), (4, 0), (1, 0), (3, 0)]))
    seed = [716]
    summary("20000 calls, values to 10^7", run(random_calls(seed, 20000, 4, 10000000)))
    summary("20000 calls, values to 5", run(random_calls(seed, 20000, 4, 5)))
    summary("10000 calls, mostly pushes", run(random_calls(seed, 10000, 6, 1000)))
    rising = [(0, i) for i in range(2000)] + [(4, 0)] * 2000
    summary("2000 rising pushes, then 2000 max pops", run(rising))


main()
