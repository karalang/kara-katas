# LeetCode #470: Implement Rand10() Using Rand7() -- rejection sampling.
# Mirror of rand10.kara (the ★ arm), with the same harness.


def rand10(rng):
    while True:
        v = (rng.rand7() - 1) * 7 + rng.rand7()
        if v <= 40:
            return 1 + (v - 1) % 10


# ---- test harness ----------------------------------------------------------


class Rand7:
    def __init__(self, seed=0, script=None):
        self.seed = seed
        self.script = script
        self.pos = 0
        self.overrun = False

    def rand7(self):
        if self.script is not None:
            if self.pos < len(self.script):
                d = self.script[self.pos]
                self.pos += 1
                return d
            self.overrun = True
            return 2
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return 1 + (self.seed // 65536) % 7


def explore(script, depth, masses):
    rng = Rand7(script=list(script))
    value = rand10(rng)
    if not rng.overrun:
        if value < 1 or value > 10:
            return False
        masses[value] += 7 ** (depth - len(script))
        return True
    if len(script) == depth:
        return True
    for d in range(1, 8):
        script.append(d)
        ok = explore(script, depth, masses)
        script.pop()
        if not ok:
            return False
    return True


def within(count, expected, variance):
    off = abs(count - expected)
    return off * off < 16 * variance


def text(b):
    return "true" if b else "false"


def main():
    in_range = True
    for depth in range(2, 7):
        masses = [0] * 11
        finished = explore([], depth, masses)
        in_range = in_range and finished
        equal = all(masses[v] == masses[1] for v in range(2, 11))
        print(f"every script of up to {depth} draws: all ten values equally likely: {text(equal)}")
    print(f"every value returned is from 1 to 10: {text(in_range)}")
    n = 1000000
    rng = Rand7(seed=470)
    counts = [0] * 11
    pairs = [0] * 100
    last = 0
    ok = True
    for i in range(n):
        value = rand10(rng)
        if value < 1 or value > 10:
            ok = False
        else:
            counts[value] += 1
            if i % 2 == 1:
                pairs[(last - 1) * 10 + value - 1] += 1
            last = value
    even = all(within(counts[v], n // 10, 90000) for v in range(1, 11))
    independent = all(within(p, n // 200, 4950) for p in pairs)
    print(f"{n} draws, all from 1 to 10: {text(ok)}")
    print(f"each value within 4 standard deviations of {n // 10}: {text(even)}")
    print(f"each of the 100 pairs of consecutive draws within 4 standard deviations of {n // 200}: {text(independent)}")


main()
