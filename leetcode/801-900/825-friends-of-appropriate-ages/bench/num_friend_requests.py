# Benchmark for #825: Friends Of Appropriate Ages -- the ★ arm (counts by age).
#
# Mirrors num_friend_requests.kara: the people counted by age once, and
# every pair of ages tested with the statement's three conditions, each
# pair that passes adding one request from every person of the first age
# to every person of the second, but for a person and themself.


def asks(x, y):
    return not (2 * y <= x + 14 or y > x or (y > 100 and x < 100))


def num_friend_requests(ages):
    count = [0] * 121
    for a in ages:
        count[a] += 1
    requests = 0
    for x in range(1, 121):
        if count[x] == 0:
            continue
        for y in range(1, 121):
            if count[y] > 0 and asks(x, y):
                requests += count[x] * count[y]
                if x == y:
                    requests -= count[x]
    return requests


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    count = 64
    rounds = 50000
    rng = Random(825)
    lists = []
    for _ in range(count):
        lists.append([1 + rng.next() % 120 for _ in range(20000)])
    total = 0
    checksum = 0
    for r in range(rounds):
        n = num_friend_requests(lists[r % count])
        total += n
        checksum = (checksum * 131 + n) % 1000000007
    print(f"{rounds} rounds of {count} lists: total {total}, checksum {checksum}")


main()
