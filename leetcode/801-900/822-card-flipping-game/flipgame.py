# LeetCode 822 — Card Flipping Game, by a set of the doubles.
#
# Mirrors flipgame.kara: a number on both sides of one card can never be
# good, and any other number on a card can, so the answer is the
# smallest number on any card that is not on both sides of one, or 0.


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


def show(fronts, backs):
    print(f"[{', '.join(map(str, fronts))}] [{', '.join(map(str, backs))}] -> {flipgame(fronts, backs)}")


def main():
    show([1, 2, 4, 4, 7], [1, 3, 4, 1, 3])
    show([1], [1])
    show([1], [2])
    show([2, 2], [2, 2])
    show([5, 3], [3, 5])
    show([1, 1, 2], [1, 2, 1])
    show([2000, 1999], [2000, 1])
    show([3, 2, 1], [3, 2, 1])
    rng = Random(822)
    fronts, backs = [], []
    for k in range(500):
        fronts.append(500 - k)
        backs.append(500 - k)
        fronts.append(1 + rng.next() % 2000)
        backs.append(1 + rng.next() % 2000)
    print(f"1000 cards, 1 to 500 doubled -> {flipgame(fronts, backs)}")
    fronts, backs = [], []
    for _ in range(1000):
        fronts.append(1 + rng.next() % 20)
        backs.append(1 + rng.next() % 20)
    print(f"1000 cards up to 20 -> {flipgame(fronts, backs)}")
    total = 0
    check = 0
    none = 0
    for _ in range(300):
        count = 1 + rng.next() % 12
        fronts, backs = [], []
        for _ in range(count):
            fronts.append(1 + rng.next() % 5)
            backs.append(1 + rng.next() % 5)
        answer = flipgame(fronts, backs)
        if answer == 0:
            none += 1
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random hands: total {total}, {none} with no good number, checksum {check}")


main()
