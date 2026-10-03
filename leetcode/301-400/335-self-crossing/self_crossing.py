# LeetCode #335: Self Crossing — three local cases.
# Python mirror of self_crossing.kara; prints the same lines.


def is_self_crossing(d):
    for i in range(3, len(d)):
        if d[i] >= d[i - 2] and d[i - 1] <= d[i - 3]:
            return True
        if i >= 4 and d[i - 1] == d[i - 3] and d[i] + d[i - 4] >= d[i - 2]:
            return True
        if (
            i >= 5
            and d[i - 2] >= d[i - 4]
            and d[i] + d[i - 4] >= d[i - 2]
            and d[i - 1] <= d[i - 3]
            and d[i - 1] + d[i - 5] >= d[i - 3]
        ):
            return True
    return False


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(d):
    shown = ", ".join(str(x) for x in d)
    print(f"[{shown}] -> {'true' if is_self_crossing(d) else 'false'}")


def main():
    show([2, 1, 1, 2])
    show([1, 2, 3, 4])
    show([1, 1, 1, 2])
    show([])
    show([1])
    show([1, 1, 1])
    show([1, 1, 2, 1, 1])
    show([3, 3, 4, 2, 2])
    show([1, 1, 2, 2, 1, 1])
    show([3, 3, 3, 2, 1, 1])
    show([1, 2, 3, 4, 5, 6, 7, 8, 9])
    show([9, 8, 7, 6, 5, 4, 3, 2, 1])
    show([1, 2, 3, 4, 3, 3, 1])
    show([2, 2, 4, 3, 3, 1, 4])
    show([1000000000, 1000000000, 1000000000, 999999999])
    rng = Rng(335)
    for rnd in range(8):
        n = 4 + rnd * 2
        show([1 + rng.next() % (3 + rnd) for _ in range(n)])
    spiral = list(range(1, 100001))
    count = len(spiral)
    out = is_self_crossing(spiral)
    spiral.append(1)
    still = is_self_crossing(spiral)
    spiral.append(100002)
    crossed = is_self_crossing(spiral)
    b = lambda v: "true" if v else "false"
    print(f"spiral: {count} moves -> {b(out)}, turn in -> {b(still)}, then out -> {b(crossed)}")


main()
