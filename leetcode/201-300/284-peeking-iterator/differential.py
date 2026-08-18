#!/usr/bin/env python3
"""LeetCode 284 — differential harness. Mirror of differential.kara.

A peeking iterator is a state machine, so the harness DRIVES all three
implementations through the same random interleavings of peek/next/has_next and
compares every response, rather than comparing one drain.
"""


class Source:
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


class Eager:
    def __init__(self, data):
        self.src = Source(data)
        self.full = False
        self.slot = 0
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


class Lazy:
    def __init__(self, data):
        self.src = Source(data)
        self.slot = 0
        self.full = False

    def peek(self):
        if not self.full:
            self.slot = self.src.next()
            self.full = True
        return self.slot

    def has_next(self):
        return self.full or self.src.has_next()

    def next(self):
        if self.full:
            self.full = False
            return self.slot
        return self.src.next()


class Materialized:
    def __init__(self, data):
        self.src = Source(data)
        self.all = []
        while self.src.has_next():
            self.all.append(self.src.next())
        self.pos = 0

    def peek(self):
        return self.all[self.pos]

    def has_next(self):
        return self.pos < len(self.all)

    def next(self):
        v = self.all[self.pos]
        self.pos += 1
        return v


def main():
    sequences = operations = 0
    has_next_mismatch = peek_mismatch = next_mismatch = peek_advanced = 0
    eager_pulls = lazy_pulls = mat_pulls = digest = 0

    seed = 20260822
    for ln in range(0, 7):
        for _ in range(120):
            data = []
            for _ in range(ln):
                seed = (seed * 1103515245 + 12345) % 2147483648
                data.append(seed % 1000)

            a, b, c = Eager(data), Lazy(data), Materialized(data)

            seed = (seed * 1103515245 + 12345) % 2147483648
            steps = (seed // 31) % (3 * ln + 7)
            for step in range(steps):
                seed = (seed * 1103515245 + 12345) % 2147483648
                op = (seed // 29) % 4

                ha, hb, hc = a.has_next(), b.has_next(), c.has_next()
                if ha != hb or ha != hc:
                    has_next_mismatch += 1
                digest = (digest * 131 + step) % 1000000007
                if ha:
                    digest = (digest + 7) % 1000000007

                all_ready = ha and hb and hc
                if op == 0:
                    operations += 1
                elif all_ready:
                    if op == 1:
                        pa, pb, pc = a.peek(), b.peek(), c.peek()
                        if pa != pb or pa != pc:
                            peek_mismatch += 1
                        digest = (digest * 131 + pa) % 1000000007
                    elif op == 2:
                        p1, p2 = a.peek(), a.peek()
                        q1, q2 = b.peek(), b.peek()
                        r1, r2 = c.peek(), c.peek()
                        if p1 != p2 or q1 != q2 or r1 != r2:
                            peek_advanced += 1
                        na, nb, nc = a.next(), b.next(), c.next()
                        if na != p1 or nb != q1 or nc != r1:
                            peek_advanced += 1
                        if na != nb or na != nc:
                            next_mismatch += 1
                        digest = (digest * 131 + na) % 1000000007
                    else:
                        na, nb, nc = a.next(), b.next(), c.next()
                        if na != nb or na != nc:
                            next_mismatch += 1
                        digest = (digest * 131 + na) % 1000000007
                    operations += 1

            eager_pulls += a.src.pulls
            lazy_pulls += b.src.pulls
            mat_pulls += c.src.pulls
            sequences += 1

    print(f"sequences {sequences}, operations executed {operations}")
    print(f"underlying pulls: eager {eager_pulls}, lazy {lazy_pulls}, materialized {mat_pulls}")
    print(f"digest {digest}")
    print(f"has_next disagreements {has_next_mismatch}")
    print(f"peek disagreements {peek_mismatch}")
    print(f"next disagreements {next_mismatch}")
    print(f"peek that advanced {peek_advanced}")


main()
