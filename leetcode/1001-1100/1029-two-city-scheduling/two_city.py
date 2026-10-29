# LeetCode #1029: Two City Scheduling -- sorted by the saving
# Mirrors two_city.kara (the ★ arm) and prints the same output.


def two_city_sched_cost(costs):
    order = sorted(costs, key=lambda c: c[0] - c[1])
    half = len(order) // 2
    total = 0
    for i, c in enumerate(order):
        total += c[0] if i < half else c[1]
    return total


seed = 1029


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(costs):
    return "[" + ",".join(f"[{a},{b}]" for a, b in costs) + "]"


def main():
    examples = [
        [[10, 20], [30, 200], [400, 50], [30, 20]],
        [[259, 770], [448, 54], [926, 667], [184, 139], [840, 118], [577, 469]],
        [[515, 563], [451, 713], [537, 709], [343, 819], [855, 779], [457, 60], [650, 359], [631, 42]],
        [[1, 1000], [1000, 1]],
        [[1, 1000], [2, 1000]],
        [[5, 5], [5, 5], [5, 5], [5, 5]],
        [[1000, 1000], [1, 1], [500, 1], [1, 500], [999, 998], [2, 3]],
    ]
    for costs in examples:
        print(f"{show(costs)} -> {two_city_sched_cost(costs)}")
    groups = [(2000, 1, 10), (1000, 3, 1000), (500, 10, 50), (200, 25, 1000), (50, 50, 1000), (20, 50, 3)]
    for count, pairs, top in groups:
        total = 0
        check = 0
        for _ in range(count):
            costs = []
            for _ in range(2 * pairs):
                a = next_random() % top + 1
                b = next_random() % top + 1
                costs.append([a, b])
            answer = two_city_sched_cost(costs)
            total += answer
            check = (check * 131 + answer) % 1000000007
        print(f"{count} cases of {2 * pairs} people (costs 1 to {top}): sum {total}, checksum {check}")
    cheap_a = [[k + 1, k + 500] for k in range(100)]
    level = [[1000, 1000] for _ in range(100)]
    print(f"100 people, a always cheaper by 499: {two_city_sched_cost(cheap_a)}")
    print(f"100 people, every cost 1000: {two_city_sched_cost(level)}")


main()
