# LeetCode #641: Design Circular Deque -- Python mirror of the ★ arm.
#
# A ring of k slots with the front value's slot and a count.


class MyCircularDeque:
    def __init__(self, k):
        self.data = [0] * k
        self.head = 0
        self.count = 0

    def insert_front(self, value):
        if self.count == len(self.data):
            return False
        self.head = (self.head + len(self.data) - 1) % len(self.data)
        self.data[self.head] = value
        self.count += 1
        return True

    def insert_last(self, value):
        if self.count == len(self.data):
            return False
        self.data[(self.head + self.count) % len(self.data)] = value
        self.count += 1
        return True

    def delete_front(self):
        if self.count == 0:
            return False
        self.head = (self.head + 1) % len(self.data)
        self.count -= 1
        return True

    def delete_last(self):
        if self.count == 0:
            return False
        self.count -= 1
        return True

    def get_front(self):
        return -1 if self.count == 0 else self.data[self.head]

    def get_rear(self):
        if self.count == 0:
            return -1
        return self.data[(self.head + self.count - 1) % len(self.data)]

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == len(self.data)


seed = 641


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
    if name == "insertFront":
        return text(q.insert_front(op[1]))
    if name == "insertLast":
        return text(q.insert_last(op[1]))
    if name == "deleteFront":
        return text(q.delete_front())
    if name == "deleteLast":
        return text(q.delete_last())
    if name == "getFront":
        return text(q.get_front())
    if name == "getRear":
        return text(q.get_rear())
    if name == "isEmpty":
        return text(q.is_empty())
    return text(q.is_full())


def run_all(k, ops):
    q = MyCircularDeque(k)
    return "[null" + "".join("," + run(q, op) for op in ops) + "]"


def show(k, ops):
    print(f"k = {k}: {run_all(k, ops)}")


def script(count):
    ops = []
    for _ in range(count):
        roll = next_random() % 40
        if roll < 8:
            ops.append(("insertFront", next_random() % 1001))
        elif roll < 16:
            ops.append(("insertLast", next_random() % 1001))
        elif roll < 21:
            ops.append(("deleteFront",))
        elif roll < 26:
            ops.append(("deleteLast",))
        elif roll < 30:
            ops.append(("getFront",))
        elif roll < 34:
            ops.append(("getRear",))
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


IF = lambda v: ("insertFront", v)
IL = lambda v: ("insertLast", v)
DF, DL, GF, GR = ("deleteFront",), ("deleteLast",), ("getFront",), ("getRear",)
EM, FU = ("isEmpty",), ("isFull",)


def main():
    show(3, [IL(1), IL(2), IF(3), IF(4), GR, FU, DL, IF(4), GF])
    show(2, [DF, DL, GF, GR, EM, FU])
    show(1, [IF(5), FU, IL(6), GF, GR, DL, EM, IL(7), GF, DF, DF])
    show(2, [IF(1), IF(2), DL, IF(3), GF, GR, DL, IF(4), GF, GR, DF, IF(5), GF, GR])
    show(4, [IL(1), IL(2), IL(3), DL, GR, DF, GF, IF(9), IL(8), GF, GR])
    show(4, [IL(0), IF(1000), IL(0), IF(1000), FU, IL(1), DF, DL, DF, GF, GR, DL, EM, GR])
    total = []
    for _ in range(300):
        k = 1 + next_random() % 8
        ops = script(1 + next_random() % 60)
        total.append(run_all(k, ops))
    print(f"300 random scripts: {summary(''.join(total))}")
    long = script(2000)
    print(f"2000 operations, k = 1000: {summary(run_all(1000, long))}")
    print(f"2000 operations, k = 1: {summary(run_all(1, long))}")


main()
