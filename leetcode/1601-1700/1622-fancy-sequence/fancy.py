# LeetCode #1622: Fancy Sequence -- the Python mirror of fancy.kara (★).
#
# Every value is stored as it would have been before all the operations so
# far: the whole sequence lies under one map x -> mul x + add, and a value
# appended under it is stored as (val - add) / mul, the division a Fermat
# inverse.

MOD = 1000000007


class Fancy:
    def __init__(self):
        self.stored = []
        self.mul = 1
        self.add = 0

    def append(self, val):
        shifted = (val - self.add + MOD) % MOD
        self.stored.append(shifted * pow(self.mul, MOD - 2, MOD) % MOD)

    def add_all(self, inc):
        self.add = (self.add + inc) % MOD

    def mult_all(self, m):
        self.mul = self.mul * m % MOD
        self.add = self.add * m % MOD

    def get_index(self, idx):
        if idx >= len(self.stored):
            return -1
        return (self.stored[idx] * self.mul + self.add) % MOD


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def replay(calls):
    fancy = Fancy()
    answers = ["null"]
    for name, arg in calls:
        if name == "append":
            fancy.append(arg)
            answers.append("null")
        elif name == "addAll":
            fancy.add_all(arg)
            answers.append("null")
        elif name == "multAll":
            fancy.mult_all(arg)
            answers.append("null")
        else:
            answers.append(str(fancy.get_index(arg)))
    print("[" + ", ".join(answers) + "]")


def batch(count, calls):
    check = 0
    misses = 0
    for _ in range(count):
        fancy = Fancy()
        length = 0
        for _ in range(calls):
            arg = next_random() % 100 + 1
            r = next_random() % 10
            if r <= 3:
                fancy.append(arg)
                length += 1
            elif r <= 5:
                fancy.add_all(arg)
            elif r <= 7:
                fancy.mult_all(arg)
            else:
                idx = wide_random() % (length + length // 4 + 1)
                got = fancy.get_index(idx)
                if got == -1:
                    misses += 1
                check = mix(check, got)
    print(f"{count} sequences of {calls} calls: {misses} reads past the end, checksum {check}")


def main():
    global seed
    replay([
        ("append", 2), ("addAll", 3), ("append", 7), ("multAll", 2),
        ("getIndex", 0), ("addAll", 3), ("append", 10), ("multAll", 2),
        ("getIndex", 0), ("getIndex", 1), ("getIndex", 2),
    ])
    replay([("getIndex", 0)])
    big = [("append", 100)] + [("multAll", 100)] * 10 + [("getIndex", 0), ("getIndex", 1)]
    replay(big)
    seed = 1622
    batch(3000, 20)
    batch(300, 300)
    batch(1, 100000)


main()
