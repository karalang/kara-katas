#!/usr/bin/env python3
"""LeetCode 284 bench mirror — Python. Same eager wrapper and operation mix."""
N = 200000
ROUNDS = 320


class Source:
    __slots__ = ("data", "pos", "pulls")

    def __init__(self, data):
        self.data = list(data)
        self.pos = 0
        self.pulls = 0

    def has_next(self):
        return self.pos < len(self.data)

    def next(self):
        v = self.data[self.pos]
        self.pos += 1
        self.pulls += 1
        return v


class Peeking:
    __slots__ = ("src", "slot", "full")

    def __init__(self, data):
        self.src = Source(data)
        self.slot = 0
        self.full = False
        if self.src.has_next():
            self.slot = self.src.next()
            self.full = True

    def peek(self):
        return self.slot

    def has_next(self):
        return self.full

    def next(self):
        v = self.slot
        if self.src.has_next():
            self.slot = self.src.next()
        else:
            self.full = False
        return v


def main():
    seed = 20260823
    data = []
    for _ in range(N):
        seed = (seed * 1103515245 + 12345) % 2147483648
        data.append(seed % 100003)
    sink = total = 0
    for _ in range(ROUNDS):
        p = Peeking(data)
        h, pos = 0, 1
        while p.has_next():
            h = (h * 31 + p.peek() * pos) % 1000000007
            h = (h * 31 + p.peek()) % 1000000007
            v = p.next()
            h = (h * 31 + v) % 1000000007
            pos += 1
        total += p.src.pulls
        sink = (sink + h) % 1000000007
    print(sink, total)


main()
