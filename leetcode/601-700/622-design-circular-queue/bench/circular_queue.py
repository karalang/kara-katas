# LeetCode #622: Design Circular Queue -- Python mirror of the Kāra bench.
#
# The ★ arm's ring with a start and a count, on the same script and
# queues.


class MyCircularQueue:
    __slots__ = ("data", "head", "count")

    def __init__(self, k):
        self.data = [0] * k
        self.head = 0
        self.count = 0

    def en_queue(self, value):
        if self.count == len(self.data):
            return False
        self.data[(self.head + self.count) % len(self.data)] = value
        self.count += 1
        return True

    def de_queue(self):
        if self.count == 0:
            return False
        self.head = (self.head + 1) % len(self.data)
        self.count -= 1
        return True

    def front(self):
        return -1 if self.count == 0 else self.data[self.head]

    def rear(self):
        if self.count == 0:
            return -1
        return self.data[(self.head + self.count - 1) % len(self.data)]

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == len(self.data)


seed = 622


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def script(count):
    ops = []
    for _ in range(count):
        roll = next_random() % 40
        if roll < 16:
            ops.append(next_random() % 1001)
        elif roll < 26:
            ops.append(-1)
        elif roll < 30:
            ops.append(-2)
        elif roll < 34:
            ops.append(-3)
        elif roll < 37:
            ops.append(-4)
        else:
            ops.append(-5)
    return ops


def main():
    rounds = 300
    ops = script(100000)
    checksum = 0
    for r in range(rounds):
        q = MyCircularQueue(1 + (r * 37) % 1000)
        for op in ops:
            if op >= 0:
                v = int(q.en_queue(op))
            elif op == -1:
                v = int(q.de_queue())
            elif op == -2:
                v = q.front()
            elif op == -3:
                v = q.rear()
            elif op == -4:
                v = int(q.is_empty())
            else:
                v = int(q.is_full())
            checksum = (checksum * 31 + v + 2) % 1000000007
    print(f"{rounds} queues, {len(ops)} operations each: checksum {checksum}")


main()
