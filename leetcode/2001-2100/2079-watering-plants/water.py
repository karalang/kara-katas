# LeetCode #2079: Watering Plants -- Python mirror of the ★ arm
# (water.kara): one step to each plant, and `2 · i` more for a plant `i`
# the can no longer covers, the can full again.


def watering_plants(plants, capacity):
    steps = 0
    can = capacity
    for i, need in enumerate(plants):
        if can < need:
            steps += 2 * i
            can = capacity
        steps += 1
        can -= need
    return steps


seed = 2079


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


examples = [
    ([2, 2, 3, 3], 5),
    ([1, 1, 1, 4, 2, 3], 4),
    ([7, 7, 7, 7, 7, 7, 7], 8),
    ([5], 5),
    ([3, 3, 3], 3),
    ([1, 2, 3, 4, 5], 100),
    ([4, 1, 1, 4, 2, 2], 6),
]
for plants, capacity in examples:
    print(f"{show(plants)}, capacity = {capacity} -> {watering_plants(plants, capacity)}")
total = 0
check = 0
for _ in range(2000):
    n = next_random() % 100 + 1
    capacity = next_random() % 50 + 1
    plants = [next_random() % capacity + 1 for _ in range(n)]
    a = watering_plants(plants, capacity)
    total += a
    check = (check * 31 + a) % 1000000007
print(f"2000 gardens: sum {total}, checksum {check}")
plants = []
for _ in range(1000):
    hi = next_random()
    plants.append((hi * 32768 + next_random()) % 1000000 + 1)
print(f"1000 plants -> {watering_plants(plants, 1000000)}")
