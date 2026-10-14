# LeetCode #622: Design Circular Queue -- Python mirror of
# circular_queue.kara.
#
# The same ring with a start and a count, and the same harness, printing
# the same lines.


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


def text(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    return str(v)


def run(q, op):
    name = op[0]
    if name == "enQueue":
        return text(q.en_queue(op[1]))
    if name == "deQueue":
        return text(q.de_queue())
    if name == "Front":
        return text(q.front())
    if name == "Rear":
        return text(q.rear())
    if name == "isEmpty":
        return text(q.is_empty())
    return text(q.is_full())


def run_all(k, ops):
    q = MyCircularQueue(k)
    return "[null" + "".join("," + run(q, op) for op in ops) + "]"


def show(k, ops):
    print(f"k = {k}: {run_all(k, ops)}")


def script(count):
    ops = []
    for _ in range(count):
        roll = next_random() % 40
        if roll < 16:
            ops.append(("enQueue", next_random() % 1001))
        elif roll < 26:
            ops.append(("deQueue",))
        elif roll < 30:
            ops.append(("Front",))
        elif roll < 34:
            ops.append(("Rear",))
        elif roll < 37:
            ops.append(("isEmpty",))
        else:
            ops.append(("isFull",))
    return ops


def summary(s):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % 1000000007
    return f"{len(s)} characters, checksum {h}"


E = lambda v: ("enQueue", v)
D, F, R, EM, FU = ("deQueue",), ("Front",), ("Rear",), ("isEmpty",), ("isFull",)


def main():
    show(3, [E(1), E(2), E(3), E(4), R, FU, D, E(4), R])
    show(2, [D, F, R, EM, FU])
    show(1, [E(5), FU, E(6), F, R, D, EM, E(7), R, D, D])
    show(2, [E(1), E(2), D, E(3), F, R, D, E(4), F, R, D, E(5), E(6), F, R])
    show(4, [E(0), E(1000), E(0), E(1000), D, D, D, F, R, EM, D, EM, F])
    total = []
    for _ in range(300):
        k = 1 + next_random() % 8
        ops = script(1 + next_random() % 60)
        total.append(run_all(k, ops))
    print(f"300 random scripts: {summary(''.join(total))}")
    long = script(3000)
    print(f"3000 operations, k = 1000: {summary(run_all(1000, long))}")
    print(f"3000 operations, k = 1: {summary(run_all(1, long))}")


main()
