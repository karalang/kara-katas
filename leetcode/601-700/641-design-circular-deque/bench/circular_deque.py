# Benchmark for #641: mirror of circular_deque.kara (the ★ arm: a ring
# with a start and a count) on the same workload.


class MyCircularDeque:
    def __init__(self, k):
        self.data = [0] * k
        self.head = 0
        self.count = 0

    def insert_front(self, value):
        n = len(self.data)
        if self.count == n:
            return False
        self.head = (self.head + n - 1) % n
        self.data[self.head] = value
        self.count += 1
        return True

    def insert_last(self, value):
        n = len(self.data)
        if self.count == n:
            return False
        self.data[(self.head + self.count) % n] = value
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


def make_random(seed):
    state = [seed]

    def next_random():
        state[0] = (state[0] * 1103515245 + 12345) % 2147483648
        return state[0] // 65536

    return next_random


def script(count, next_random):
    ops = []
    for _ in range(count):
        roll = next_random() % 40
        if roll < 8:
            ops.append(next_random() % 1001)
        elif roll < 16:
            ops.append(1001 + next_random() % 1001)
        elif roll < 21:
            ops.append(-1)
        elif roll < 26:
            ops.append(-2)
        elif roll < 30:
            ops.append(-3)
        elif roll < 34:
            ops.append(-4)
        elif roll < 37:
            ops.append(-5)
        else:
            ops.append(-6)
    return ops


def main():
    rounds = 300
    ops = script(100000, make_random(641))
    checksum = 0
    for r in range(rounds):
        q = MyCircularDeque(1 + (r * 37) % 1000)
        for op in ops:
            if op >= 1001:
                v = int(q.insert_last(op - 1001))
            elif op >= 0:
                v = int(q.insert_front(op))
            elif op == -1:
                v = int(q.delete_front())
            elif op == -2:
                v = int(q.delete_last())
            elif op == -3:
                v = q.get_front()
            elif op == -4:
                v = q.get_rear()
            elif op == -5:
                v = int(q.is_empty())
            else:
                v = int(q.is_full())
            checksum = (checksum * 31 + v + 2) % 1000000007
    print(f"{rounds} deques, {len(ops)} operations each: checksum {checksum}")


if __name__ == "__main__":
    main()
