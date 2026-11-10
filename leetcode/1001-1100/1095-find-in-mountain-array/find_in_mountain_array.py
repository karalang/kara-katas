# LeetCode #1095: Find in Mountain Array -- Python mirror of the ★ arm:
# three binary searches, the peak, then the rising side, then the falling
# side, through a counted `get`. Same cases and output as
# find_in_mountain_array.kara.


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


def ask(target, values):
    m = MountainArray(values)
    at = find_in_mountain_array(target, m)
    return at, m.calls <= 100


def mountain(up, down, step):
    v = [down * step + next_random() % 20]
    for _ in range(up):
        v.append(v[-1] + 1 + next_random() % step)
    for _ in range(down):
        v.append(v[-1] - 1 - next_random() % step)
    return v


def show(b):
    return "true" if b else "false"


cases = [
    (3, [1, 2, 3, 4, 5, 3, 1]),
    (3, [0, 1, 2, 4, 2, 1]),
    (1, [0, 1, 0]),
    (0, [0, 1, 0]),
    (2, [0, 1, 0]),
    (5, [1, 5, 2]),
    (2, [1, 5, 2]),
    (1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]),
    (1, [1, 9, 8, 7, 6, 5, 4, 3, 2, 1]),
    (4, [1, 3, 5, 7, 5, 3, 1]),
    (1000000000, [0, 1000000000, 999999999]),
]
for target, values in cases:
    at, within = ask(target, list(values))
    print(f"{at} {show(within)}")
found = over = check = 0
for _ in range(2000):
    up = 1 + next_random() % 30
    down = 1 + next_random() % 30
    step = 1 + next_random() % 4
    values = mountain(up, down, step)
    k = next_random() % len(values)
    target = values[k] + next_random() % 3 - 1
    at, within = ask(target, values)
    if at >= 0:
        found += 1
    if not within:
        over += 1
    check = (check * 31 + at + 1) % 1000000007
print(f"2000 random mountains: {found} found, {over} over 100 calls, checksum {check}")
for up in [9997, 5000, 2]:
    values = mountain(up, 9999 - up, 50000)
    peak = values[up]
    for target in [values[up // 2], peak, values[(up + 9999) // 2], values[9999]]:
        at, within = ask(target, list(values))
        print(f"10^4 values, peak at {up}: {at} {show(within)}")
