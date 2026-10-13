# Benchmark for #470: mirror of rand10.kara (the ★ arm: rejection
# sampling) on the same workload, over the same seeded rand7.


class Rand7:
    def __init__(self, seed):
        self.seed = seed

    def rand7(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return 1 + (self.seed // 65536) % 7


def rand10(rng):
    while True:
        v = (rng.rand7() - 1) * 7 + rng.rand7()
        if v <= 40:
            return 1 + (v - 1) % 10


def main():
    n = 20000000
    rng = Rand7(470)
    counts = [0] * 11
    checksum = 0
    for _ in range(n):
        value = rand10(rng)
        counts[value] += 1
        checksum = (checksum * 11 + value) % 1000000007
    print(f"{n} draws: {counts[1]} ones, {counts[10]} tens, checksum {checksum}")


main()
