# LeetCode #881: Boats to Save People -- Python mirror of the ★ arm (sort,
# then two pointers) and its test harness; prints the same output as
# num_rescue_boats.kara.


def num_rescue_boats(people, limit):
    weights = sorted(people)
    light = 0
    heavy = len(weights) - 1
    boats = 0
    while light <= heavy:
        if weights[light] + weights[heavy] <= limit:
            light += 1
        heavy -= 1
        boats += 1
    return boats


# ---- test harness ----------------------------------------------------------


def text(values):
    if len(values) > 6:
        return f"[{values[0]}, {values[1]}, ... ({len(values)} people)]"
    return "[" + ", ".join(str(v) for v in values) + "]"


def show(people, limit):
    print(f"people = {text(people)}, limit = {limit} -> {num_rescue_boats(people, limit)}")


seed = 881


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([1, 2], 3)
    show([3, 2, 2, 1], 3)
    show([3, 5, 3, 4], 5)
    show([7], 7)
    show([5, 5, 5, 5, 5], 10)
    show([1, 9, 2, 8, 3, 7, 4, 6, 5], 10)
    show([6, 6, 6, 6], 11)
    show([15000] * 50000, 30000)
    show([30000] * 50000, 30000)
    show([i % 30000 + 1 for i in range(50000)], 30000)
    total = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        limit = next_random() % 20 + 1
        people = [next_random() % limit + 1 for _ in range(n)]
        total += num_rescue_boats(people, limit)
    print(f"3000 cases of 1 to 12 people: {total} boats")
    total = 0
    check = 0
    for _ in range(10):
        n = 40000 + next_random() % 10001
        limit = 1 + (next_random() * 32768 + next_random()) % 30000
        people = []
        for _ in range(n):
            x = next_random()
            y = next_random()
            people.append((x * 32768 + y) % limit + 1)
        boats = num_rescue_boats(people, limit)
        total += boats
        check = (check * 131 + boats) % 1000000007
    print(f"10 cases of up to 50000 people: {total} boats, checksum {check}")


main()
