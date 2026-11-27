# LeetCode #1825: Finding MK Average -- the ★ arm in Python, with each bag a
# dict of counts and its least and largest found by sorting its keys
import bisect


class Bag:
    def __init__(self):
        self.keys = []
        self.counts = {}
        self.size = 0
        self.sum = 0

    def add(self, x):
        if x not in self.counts:
            bisect.insort(self.keys, x)
            self.counts[x] = 0
        self.counts[x] += 1
        self.size += 1
        self.sum += x

    def remove(self, x):
        self.counts[x] -= 1
        if self.counts[x] == 0:
            del self.counts[x]
            self.keys.pop(bisect.bisect_left(self.keys, x))
        self.size -= 1
        self.sum -= x

    def holds(self, x):
        return x in self.counts

    def least(self):
        return self.keys[0]

    def most(self):
        return self.keys[-1]


class MkAverage:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.window = []
        self.start = 0
        self.low, self.mid, self.high = Bag(), Bag(), Bag()

    def add_element(self, num):
        self.window.append(num)
        n = len(self.window) - self.start
        if n < self.m:
            return
        if n == self.m:
            s = sorted(self.window[self.start:])
            for i in range(n):
                if i < self.k:
                    self.low.add(s[i])
                elif i >= n - self.k:
                    self.high.add(s[i])
                else:
                    self.mid.add(s[i])
            return
        old = self.window[self.start]
        self.start += 1
        if self.low.holds(old):
            self.low.remove(old)
        elif self.high.holds(old):
            self.high.remove(old)
        else:
            self.mid.remove(old)
        if self.low.size > 0 and num <= self.low.most():
            self.low.add(num)
        elif self.high.size > 0 and num >= self.high.least():
            self.high.add(num)
        else:
            self.mid.add(num)
        while self.low.size > self.k:
            x = self.low.most(); self.low.remove(x); self.mid.add(x)
        while self.high.size > self.k:
            x = self.high.least(); self.high.remove(x); self.mid.add(x)
        while self.low.size < self.k:
            x = self.mid.least(); self.mid.remove(x); self.low.add(x)
        while self.high.size < self.k:
            x = self.mid.most(); self.mid.remove(x); self.high.add(x)

    def calculate_mk_average(self):
        if len(self.window) - self.start < self.m:
            return -1
        return self.mid.sum // (self.m - 2 * self.k)


seed = 1825


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def run(m, k, ops):
    avg = MkAverage(m, k)
    out = []
    for op in ops:
        if op < 0:
            out.append(avg.calculate_mk_average())
        else:
            avg.add_element(op)
    return out


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


print(show(run(3, 1, [3, 1, -1, 10, -1, 5, 5, 5, -1])))
print(show(run(3, 1, [7, 7, 7, -1])), show(run(4, 1, [100, 90, 1, 2, -1, 3, -1, 4, -1, 5, -1])), show(run(3, 1, [100000, 100000, 1, -1])), show(run(7, 3, [5, 1, 9, 2, 8, 3, 7, -1, 4, -1])))
ops = []
for i in range(99990):
    hi = next_random()
    ops.append(1 + (hi * 32768 + next_random()) % 100000)
    if i % 9999 == 9998:
        ops.append(-1)
print(f"the most: {show(run(50000, 10000, ops))}")
print(f"the most again: {show(run(99000, 1, ops))}")
check = 0
asked = 0
for _ in range(300):
    m = 3 + next_random() % 8
    k = 1 + next_random() % ((m - 1) // 2)
    ln = 1 + next_random() % 60
    ops = [-1 if next_random() % 3 == 0 else 1 + next_random() % 20 for _ in range(ln)]
    for x in run(m, k, ops):
        asked += 1
        check = (check * 31 + x + 2) % 1000000007
print(f"300 random runs: {asked} averages, checksum {check}")
