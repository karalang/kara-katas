# LeetCode #1670: Design Front Middle Back Queue -- the bench's Python
# mirror: the ★ arm on one run of 1000000 calls, a push three times in
# five, values up to 10^9, drawn first and then replayed 60 times, each on
# a new queue.

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


# ---- the harness ----------------------------------------------------------

seed = 1670


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


rounds = 60
calls = 1000000
run = []
for _ in range(calls):
    r = next_random() % 10
    op = r // 2 if r < 6 else r - 3
    val = (next_random() * 32768 + next_random()) % 1000000000 + 1
    run.append((op, val))
empty = 0
left = 0
check = 0
for _ in range(rounds):
    queue = FrontMiddleBackQueue()
    for op, val in run:
        if op == 0:
            queue.push_front(val)
            continue
        if op == 1:
            queue.push_middle(val)
            continue
        if op == 2:
            queue.push_back(val)
            continue
        if op == 3:
            got = queue.pop_front()
        elif op == 4:
            got = queue.pop_middle()
        else:
            got = queue.pop_back()
        if got == -1:
            empty += 1
        check = (check * 31 + got + 1) % 1000000007
    left += len(queue.front) + len(queue.back)
print(f"{calls} calls, {rounds} rounds: {empty} pops on an empty queue, {left} values left, checksum {check}")
