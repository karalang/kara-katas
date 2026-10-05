# LeetCode #346: Moving Average from Data Stream — Python mirror of the ★ arm.
from collections import deque


class MovingAverage:
    def __init__(self, size):
        self.size = size
        self.window = deque()
        self.sum = 0

    def next(self, val):
        self.window.append(val)
        self.sum += val
        if len(self.window) > self.size:
            self.sum -= self.window.popleft()
        return self.sum / len(self.window)


def run(size, vals):
    m = MovingAverage(size)
    out = ", ".join(f"{m.next(v):.5f}" for v in vals)
    print(f"size {size}: [{out}]")


def main():
    run(3, [1, 10, 3, 5])
    run(1, [4, -2, 7])
    run(10, [1, 2, 3, 4])
    run(2, [-5, 5, -5, 5, 0])
    run(3, [1, 1, 2])
    m = MovingAverage(1000)
    last = 0.0
    total = 0.0
    for k in range(100000):
        last = m.next((k * 7919) % 200001 - 100000)
        total += last
    print(f"100000 values, window 1000: last {last:.5f}, sum of averages {total:.3f}")


main()
