# LeetCode #1825: Finding MK Average -- the bench in Python: the fenwick arm
# over 20 calls on windows of 1000 to 49999 numbers, each call adding the same
# 10^5 numbers of 1 to 10^5, built once, and asking for the average after
# every hundredth; each window and its cut are drawn from the checksum so far.
# The Fenwick trees are the arm every mirror language writes the same way; the
# ★ arm's ordered bags have no counterpart in C, Go or Python's standard
# library.
from collections import deque

TOP = 100000


class MkAverage:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.window = deque()
        self.count = [0] * (TOP + 1)
        self.total = [0] * (TOP + 1)

    def change(self, x, by):
        i = x
        while i <= TOP:
            self.count[i] += by
            self.total[i] += by * x
            i += i & -i

    # the sum of the t smallest numbers of the window
    def smallest(self, t):
        at, left, total, step = 0, t, 0, 1 << 16
        while step > 0:
            if at + step <= TOP and self.count[at + step] <= left:
                at += step
                left -= self.count[at]
                total += self.total[at]
            step //= 2
        return total + left * (at + 1)

    def add_element(self, num):
        self.window.append(num)
        self.change(num, 1)
        if len(self.window) > self.m:
            self.change(self.window.popleft(), -1)

    def calculate_mk_average(self):
        if len(self.window) < self.m:
            return -1
        return (self.smallest(self.m - self.k) - self.smallest(self.k)) // (self.m - 2 * self.k)


seed = 1825


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


nums = []
for _ in range(100000):
    hi = next_random()
    nums.append(1 + (hi * 32768 + next_random()) % 100000)
check = 0
for call in range(20):
    m = 1000 + (check + call) % 49000
    k = 1 + (check * 7 + call) % ((m - 1) // 2)
    avg = MkAverage(m, k)
    for i, x in enumerate(nums):
        avg.add_element(x)
        if i % 100 == 99:
            check = (check * 31 + avg.calculate_mk_average() + 2) % 1000000007
print(f"20 calls: checksum {check}")
