# Benchmark workload for LeetCode #346 — Python mirror of moving_average.kara.
from collections import deque

LEN = 10000000
WINDOW = 1000


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


def main():
    m = MovingAverage(WINDOW)
    seed = 346
    sink = 0.0
    for _ in range(LEN):
        seed = (seed * 1103515245 + 12345) % 2147483648
        sink += m.next(seed // 16 % 200001 - 100000)
    print(f"sink {sink:.3f}")


main()
