# LeetCode #1622: Fancy Sequence -- the bench in Python, mirroring
# fancy.kara: every value stored under the inverse of one map
# x -> mul x + add, the inverse a Fermat power per append.

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


seed = 1622


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sequences = []
    for _ in range(50):
        calls = []
        length = 0
        for _ in range(100000):
            arg = next_random() % 100 + 1
            r = next_random() % 10
            if r <= 3:
                calls.append((0, arg))
                length += 1
            elif r <= 5:
                calls.append((1, arg))
            elif r <= 7:
                calls.append((2, arg))
            else:
                high = next_random()
                idx = (high * 32768 + next_random()) % (length + length // 4 + 1)
                calls.append((3, idx))
        sequences.append(calls)
    check = 0
    misses = 0
    for calls in sequences:
        fancy = Fancy()
        for kind, arg in calls:
            if kind == 0:
                fancy.append(arg)
            elif kind == 1:
                fancy.add_all(arg)
            elif kind == 2:
                fancy.mult_all(arg)
            else:
                got = fancy.get_index(arg)
                if got == -1:
                    misses += 1
                check = (check * 31 + got + 1) % 1000000007
    print(f"50 sequences of 100000 calls: {misses} reads past the end, checksum {check}")


main()
