# LeetCode #1533: Find the Index of the Large Integer -- Python mirror of
# index.kara (the ternary search); output byte-identical.


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


def array(n, base, large, at):
    values = [base] * n
    values[at] = large
    return values


def batch(count, most):
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (most - 1) + 2
        base = next_random() % 99 + 1
        large = base + next_random() % (100 - base) + 1
        at = (next_random() * 32768 + next_random()) % n
        check = mix(check, get_index(ArrayReader(array(n, base, large, at))))
    print(f"{count} arrays of 2 to {most} values: checksum {check}")


for values in [[7, 7, 7, 7, 10, 7, 7, 7], [6, 6, 12], [1, 2], [2, 1], [99, 100, 99]]:
    print(f"[{', '.join(map(str, values))}] -> {get_index(ArrayReader(values))}")
for at in [0, 1, 249999, 250000, 499998, 499999]:
    print(f"500000 values, the larger at {at} -> {get_index(ArrayReader(array(500000, 1, 2, at)))}")
batch(3000, 12)
batch(300, 1000)
batch(30, 500000)
