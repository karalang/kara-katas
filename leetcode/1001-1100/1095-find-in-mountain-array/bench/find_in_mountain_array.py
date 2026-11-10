# Benchmark: LeetCode #1095 Find in Mountain Array -- Python mirror of
# find_in_mountain_array.kara: the ★ arm's three binary searches through a
# counted `get`, over 64 mountains of 10^4 values built once, 100 rounds of
# 64 targets each.


class MountainArray:
    def __init__(self, values):
        self.values = values
        self.calls = 0

    def get(self, index):
        self.calls += 1
        return self.values[index]

    def length(self):
        return len(self.values)


def find_in_mountain_array(target, mountain):
    n = mountain.length()
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mountain.get(mid) < mountain.get(mid + 1):
            lo = mid + 1
        else:
            hi = mid
    peak = lo
    lo, hi = 0, peak
    while lo <= hi:
        mid = (lo + hi) // 2
        v = mountain.get(mid)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    lo, hi = peak + 1, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = mountain.get(mid)
        if v == target:
            return mid
        if v > target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


seed = 1095


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    mountains = []
    for j in range(64):
        up = 1 + j * 9997 // 63
        down = 9999 - up
        v = [down * 50000 + next_random() % 20]
        for _ in range(up):
            v.append(v[-1] + 1 + next_random() % 50000)
        for _ in range(down):
            v.append(v[-1] - 1 - next_random() % 50000)
        mountains.append(MountainArray(v))
    found = 0
    check = 0
    for rnd in range(100):
        for m in mountains:
            for q in range(64):
                k = (rnd * 7919 + q * 104729) % 10000
                target = m.values[k] + (rnd + q) % 3 - 1
                at = find_in_mountain_array(target, m)
                if at >= 0:
                    found += 1
                check = (check * 31 + at + 1) % 1000000007
    calls = sum(m.calls for m in mountains)
    print(f"100 rounds over 64 mountains of 10^4 values: {found} of 409600 found, {calls} calls of get, checksum {check}")


main()
