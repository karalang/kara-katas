"""Benchmark workload for LeetCode #232 — Implement Queue using Stacks (Python; scale lane)."""


class MyQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):
        self.inbox.append(x)

    def refill(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self):
        self.refill()
        return self.outbox.pop()

    def peek(self):
        self.refill()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox


def main():
    n = 75000000
    cap = 4096
    mask = 1048575

    q = MyQueue()
    sz = 0
    sink = 0
    state = 12345

    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        if q.empty() or (state % 2 == 0 and sz < cap):
            q.push(state & mask)
            sz += 1
        elif state % 4 == 0:
            sink += q.peek()
        else:
            sink += q.pop()
            sz -= 1
    print(sink)


main()
