# Benchmark for #822: Card Flipping Game -- the ★ arm (a set of the doubles).
#
# Mirrors flipgame.kara: the numbers on both sides of one card go in a
# set, and the answer is the smallest number on any card that is not in
# it, or 0.


def flipgame(fronts, backs):
    doubles = set()
    for i in range(len(fronts)):
        if fronts[i] == backs[i]:
            doubles.add(fronts[i])
    best = 0
    for i in range(len(fronts)):
        for x in (fronts[i], backs[i]):
            if x not in doubles and (best == 0 or x < best):
                best = x
    return best


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    count = 64
    rounds = 50000
    rng = Random(822)
    all_fronts, all_backs = [], []
    for _ in range(count):
        fronts, backs = [], []
        for _ in range(1000):
            f = 1 + rng.next() % 2000
            fronts.append(f)
            if rng.next() % 2 == 0:
                backs.append(f)
            else:
                backs.append(1 + rng.next() % 2000)
        all_fronts.append(fronts)
        all_backs.append(backs)
    total = 0
    checksum = 0
    for r in range(rounds):
        g = r % count
        answer = flipgame(all_fronts[g], all_backs[g])
        total += answer
        checksum = (checksum * 131 + answer) % 1000000007
    print(f"{rounds} rounds of {count} hands: total {total}, checksum {checksum}")


main()
