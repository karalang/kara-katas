# LeetCode #881 bench: Python mirror of num_rescue_boats.kara (the ★ arm,
# sort, then two pointers) on the same 600 cases.


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


seed = 881


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    total = 0
    check = 0
    for _ in range(600):
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
    print(f"600 cases of up to 50000 people: {total} boats, checksum {check}")


main()
