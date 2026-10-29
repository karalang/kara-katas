# LeetCode #1029: Two City Scheduling -- bench
# Mirrors ./two_city.kara; see ../README.md § Benchmarks.


def two_city_sched_cost(costs):
    order = [c[:] for c in costs]
    order.sort(key=lambda c: c[0] - c[1])
    half = len(order) // 2
    total = 0
    for i in range(len(order)):
        total += order[i][0] if i < half else order[i][1]
    return total


seed = 1029


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 1000, 100
    cases = []
    for _ in range(count):
        costs = []
        for _ in range(100):
            a = next_random() % 1000 + 1
            b = next_random() % 1000 + 1
            costs.append([a, b])
        cases.append(costs)
    total = 0
    check = 0
    for _ in range(rounds):
        for costs in cases:
            answer = two_city_sched_cost(costs)
            total += answer
            check = (check * 131 + answer) % 1000000007
    print(f"{count} cases of 100 people, {rounds} rounds: sum {total}, checksum {check}")


main()
