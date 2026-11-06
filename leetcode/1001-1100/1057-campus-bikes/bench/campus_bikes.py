# LeetCode #1057: Campus Bikes -- the benchmark, mirror of campus_bikes.kara.


def assign_bikes(workers, bikes):
    buckets = [[] for _ in range(2000)]
    for w, (wx, wy) in enumerate(workers):
        for b, (bx, by) in enumerate(bikes):
            d = abs(wx - bx) + abs(wy - by)
            buckets[d].append((w, b))
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_places(count, seed):
    places = []
    for _ in range(count):
        x = next_random(seed) % 1000
        y = next_random(seed) % 1000
        places.append((x, y))
    return places


def main():
    count, rounds = 20, 8
    seed = [1057]
    campuses = []
    for _ in range(count):
        workers = random_places(300, seed)
        bikes = random_places(400, seed)
        campuses.append((workers, bikes))
    ridden = 0
    check = 0
    for _ in range(rounds):
        for workers, bikes in campuses:
            answer = assign_bikes(workers, bikes)
            for w, b in enumerate(answer):
                ridden += abs(workers[w][0] - bikes[b][0]) + abs(workers[w][1] - bikes[b][1])
                check = (check * 131 + b + 1) % 1000000007
    print(f"{count} campuses of 300 workers and 400 bikes, {rounds} rounds: {ridden} ridden, checksum {check}")


main()
