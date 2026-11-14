# LeetCode #1533: Find the Index of the Large Integer -- bench: the ★ arm
# (ternary search) over 100 readers of 2 to 100000 values, built once, each
# searched 20000 times. Python mirror of index.kara.


class ArrayReader:
    def __init__(self, values):
        self.sums = [0]
        for v in values:
            self.sums.append(self.sums[-1] + v)
        self.calls = 0

    def compareSub(self, l, r, x, y):
        self.calls += 1
        left = self.sums[r + 1] - self.sums[l]
        right = self.sums[y + 1] - self.sums[x]
        return 1 if left > right else -1 if left < right else 0

    def length(self):
        return len(self.sums) - 1


def get_index(reader):
    lo, hi = 0, reader.length() - 1
    while lo < hi:
        third = (hi - lo + 1) // 3
        if third == 0:
            return lo if reader.compareSub(lo, lo, hi, hi) > 0 else hi
        second = lo + third
        c = reader.compareSub(lo, second - 1, second, second + third - 1)
        if c == 1:
            hi = second - 1
        elif c == -1:
            lo, hi = second, second + third - 1
        else:
            lo = second + third
    return lo


seed = 1533


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


readers = []
for _ in range(100):
    n = (next_random() * 32768 + next_random()) % 99999 + 2
    base = next_random() % 99 + 1
    large = base + next_random() % (100 - base) + 1
    at = (next_random() * 32768 + next_random()) % n
    values = [base] * n
    values[at] = large
    readers.append(ArrayReader(values))
check = 0
for _ in range(20000):
    for reader in readers:
        check = mix(check, get_index(reader))
calls = sum(r.calls for r in readers)
print(f"20000 passes over 100 readers of up to 100000 values: checksum {check}, {calls} calls")
