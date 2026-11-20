# LeetCode #1670: Design Front Middle Back Queue -- the Python mirror of the
# ★ arm: two deques, the back half as long as the front or one longer.

from collections import deque


class FrontMiddleBackQueue:
    def __init__(self):
        self.front = deque()
        self.back = deque()

    def balance(self):
        if len(self.front) > len(self.back):
            self.back.appendleft(self.front.pop())
        elif len(self.back) > len(self.front) + 1:
            self.front.append(self.back.popleft())

    def push_front(self, val):
        self.front.appendleft(val)
        self.balance()

    def push_middle(self, val):
        self.front.append(val)
        self.balance()

    def push_back(self, val):
        self.back.append(val)
        self.balance()

    def pop_front(self):
        if self.front:
            val = self.front.popleft()
        elif self.back:
            val = self.back.popleft()
        else:
            return -1
        self.balance()
        return val

    def pop_middle(self):
        if len(self.front) == len(self.back):
            if not self.front:
                return -1
            val = self.front.pop()
        else:
            val = self.back.popleft()
        self.balance()
        return val

    def pop_back(self):
        if not self.back:
            return -1
        val = self.back.pop()
        self.balance()
        return val


# ---- the harness: the same as the Kāra arms -------------------------------

seed = 1670


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def call(queue, op, val):
    if op == 0:
        queue.push_front(val)
    elif op == 1:
        queue.push_middle(val)
    elif op == 2:
        queue.push_back(val)
    elif op == 3:
        return queue.pop_front()
    elif op == 4:
        return queue.pop_middle()
    else:
        return queue.pop_back()
    return 0


def batch(count, calls):
    empty = 0
    check = 0
    for _ in range(count):
        queue = FrontMiddleBackQueue()
        for _ in range(calls):
            op = next_random() % 6
            val = (next_random() * 32768 + next_random()) % 1000000000 + 1
            got = call(queue, op, val)
            if op >= 3:
                if got == -1:
                    empty += 1
                check = (check * 31 + got + 1) % 1000000007
    print(f"{count} runs of {calls} calls: {empty} pops on an empty queue, checksum {check}")


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


q = FrontMiddleBackQueue()
q.push_front(1)
q.push_back(2)
q.push_middle(3)
q.push_middle(4)
print(show([q.pop_front(), q.pop_middle(), q.pop_middle(), q.pop_back(), q.pop_front()]))
q = FrontMiddleBackQueue()
for v in range(1, 7):
    q.push_back(v)
q.push_middle(7)
print(show([q.pop_middle() for _ in range(8)]))
q = FrontMiddleBackQueue()
for v in range(1, 6):
    q.push_back(v)
q.push_middle(7)
print(show([q.pop_back() for _ in range(7)]))
batch(3000, 20)
batch(300, 1000)
batch(3, 100000)
