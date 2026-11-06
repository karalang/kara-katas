# LeetCode #1057: Campus Bikes -- mirror of campus_bikes.kara.


def assign_bikes(workers, bikes):
    buckets = [[] for _ in range(2000)]
    for w, (wx, wy) in enumerate(workers):
        for b, (bx, by) in enumerate(bikes):
            buckets[abs(wx - bx) + abs(wy - by)].append((w, b))
    bike_of = [-1] * len(workers)
    taken = [False] * len(bikes)
    left = len(workers)
    for bucket in buckets:
        for w, b in bucket:
            if left > 0 and bike_of[w] < 0 and not taken[b]:
                bike_of[w] = b
                taken[b] = True
                left -= 1
    return bike_of


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_places(count, side, rng):
    places = []
    for _ in range(count):
        x = rng.next() % side
        y = rng.next() % side
        places.append((x, y))
    return places


def trial(count, most, side, rng):
    total = 0
    check = 0
    for _ in range(count):
        n = rng.next() % most + 1
        m = n + rng.next() % 4
        workers = random_places(n, side, rng)
        bikes = random_places(m, side, rng)
        answer = assign_bikes(workers, bikes)
        for w, b in enumerate(answer):
            total += abs(workers[w][0] - bikes[b][0]) + abs(workers[w][1] - bikes[b][1])
            check = (check * 131 + b + 1) % 1000000007
    return total, check


def show(places):
    return "[" + ", ".join(f"({x}, {y})" for x, y in places) + "]"


def main():
    examples = [
        ([(0, 0), (2, 1)], [(1, 2), (3, 3)]),
        ([(0, 0), (1, 1), (2, 0)], [(1, 0), (2, 2), (2, 1)]),
        ([(0, 0)], [(5, 5)]),
        ([(0, 0), (0, 0)], [(1, 1), (1, 1)]),
        ([(0, 0), (4, 0)], [(2, 0), (9, 9)]),
        ([(3, 3), (0, 0)], [(3, 2), (0, 1), (3, 4)]),
        ([(1, 1), (2, 2), (3, 3)], [(3, 3), (2, 2), (1, 1)]),
        ([(0, 0), (999, 999)], [(999, 999), (0, 0), (500, 500)]),
    ]
    for workers, bikes in examples:
        answer = assign_bikes(workers, bikes)
        print(f"{show(workers)} {show(bikes)} -> [{', '.join(map(str, answer))}]")
    rng = Rng(1057)
    total, check = trial(3000, 8, 6, rng)
    print(f"3000 campuses of 1 to 8 workers on 6 by 6: total {total}, checksum {check}")
    total, check = trial(20, 200, 1000, rng)
    print(f"20 campuses of 1 to 200 workers on 1000 by 1000: total {total}, checksum {check}")
    workers = random_places(1000, 1000, rng)
    bikes = random_places(1000, 1000, rng)
    answer = assign_bikes(workers, bikes)
    ridden = 0
    check = 0
    for w, b in enumerate(answer):
        ridden += abs(workers[w][0] - bikes[b][0]) + abs(workers[w][1] - bikes[b][1])
        check = (check * 131 + b + 1) % 1000000007
    print(f"1000 workers and 1000 bikes: {ridden} ridden, checksum {check}, first {answer[0]}, last {answer[999]}")
    workers = [(500, 500)] * 200
    bikes = random_places(1000, 1000, rng)
    answer = assign_bikes(workers, bikes)
    check = 0
    for b in answer:
        check = (check * 131 + b + 1) % 1000000007
    print(f"200 workers at one place, 1000 bikes: checksum {check}, first {answer[0]}, last {answer[199]}")


main()
