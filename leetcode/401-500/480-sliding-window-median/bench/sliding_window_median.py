# Benchmark for #480: Python mirror of the ★ arm (two heaps, deletions
# put off); see sliding_window_median.kara.
import heapq


class Window:
    def __init__(self):
        self.low = []  # largest first: values negated
        self.high = []
        self.gone = {}
        self.low_size = 0
        self.high_size = 0

    def prune(self):
        while self.low:
            top = -self.low[0]
            left = self.gone.get(top, 0)
            if left == 0:
                break
            self.gone[top] = left - 1
            heapq.heappop(self.low)
        while self.high:
            top = self.high[0]
            left = self.gone.get(top, 0)
            if left == 0:
                break
            self.gone[top] = left - 1
            heapq.heappop(self.high)

    def balance(self):
        if self.low_size > self.high_size + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))
            self.low_size -= 1
            self.high_size += 1
        elif self.low_size < self.high_size:
            heapq.heappush(self.low, -heapq.heappop(self.high))
            self.high_size -= 1
            self.low_size += 1
        self.prune()

    def add(self, x):
        if not self.low or x <= -self.low[0]:
            heapq.heappush(self.low, -x)
            self.low_size += 1
        else:
            heapq.heappush(self.high, x)
            self.high_size += 1
        self.balance()

    def remove(self, x):
        in_low = x <= -self.low[0]
        self.gone[x] = self.gone.get(x, 0) + 1
        if in_low:
            self.low_size -= 1
        else:
            self.high_size -= 1
        self.prune()
        self.balance()

    def median(self, k):
        a = -self.low[0]
        if k % 2 == 1:
            return float(a)
        return (a + self.high[0]) / 2.0


def median_sliding_window(nums, k):
    window = Window()
    medians = []
    for i in range(len(nums)):
        window.add(nums[i])
        if i >= k:
            window.remove(nums[i - k])
        if i >= k - 1:
            medians.append(window.median(k))
    return medians


seed = 480


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 1000000
    nums = []
    for _ in range(n):
        a = next_random()
        b = next_random()
        r = a * 32768 + b
        nums.append(r * 4 + next_random() % 4 - 2147483648)
    windows = 0
    checksum = 0
    for k in range(1000, 1002):
        for m in median_sliding_window(nums, k):
            windows += 1
            checksum = (checksum * 31 + int(m * 2.0) % 1000000007 + 1000000007) % 1000000007
    print(f"{windows} windows: checksum {checksum}")


main()
