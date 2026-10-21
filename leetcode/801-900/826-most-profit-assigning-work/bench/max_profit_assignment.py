# Benchmark for #826: Most Profit Assigning Work -- the ★ arm (two sorted sweeps).
#
# Mirrors max_profit_assignment.kara: the jobs paired and sorted by
# difficulty (then profit) and a copy of the workers sorted, then one
# pointer walks the jobs as the abilities grow, keeping the best profit
# among the jobs passed.


def max_profit_assignment(difficulty, profit, worker):
    n = len(difficulty)
    jobs = sorted(zip(difficulty, profit))
    abilities = sorted(worker)
    nxt = 0
    best = 0
    total = 0
    for ability in abilities:
        while nxt < n and jobs[nxt][0] <= ability:
            best = max(best, jobs[nxt][1])
            nxt += 1
        total += best
    return total


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    count = 64
    rounds = 2000
    rng = Random(826)
    difficulties = []
    profits = []
    workers = []
    for _ in range(count):
        difficulties.append([1 + rng.next() % 100000 for _ in range(10000)])
        profits.append([1 + rng.next() % 100000 for _ in range(10000)])
        workers.append([1 + rng.next() % 100000 for _ in range(10000)])
    total = 0
    checksum = 0
    for r in range(rounds):
        g = r % count
        n = max_profit_assignment(difficulties[g], profits[g], workers[g])
        total += n
        checksum = (checksum * 131 + n) % 1000000007
    print(f"{rounds} rounds of {count} cases: total {total}, checksum {checksum}")


main()
