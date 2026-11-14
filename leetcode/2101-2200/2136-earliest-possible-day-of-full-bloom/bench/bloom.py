# LeetCode #2136: Earliest Possible Day of Full Bloom -- the benchmark,
# the same algorithm as bloom.kara.


def earliest_full_bloom(plant_time, grow_time):
    order = sorted(range(len(plant_time)), key=lambda i: -grow_time[i])
    planted = 0
    bloom = 0
    for i in order:
        planted += plant_time[i]
        bloom = max(bloom, planted + grow_time[i])
    return bloom


seed = 2136


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    plants = []
    grows = []
    for _ in range(10):
        plant = []
        grow = []
        for _ in range(100000):
            plant.append(next_random() % 10000 + 1)
            grow.append(next_random() % 10000 + 1)
        plants.append(plant)
        grows.append(grow)
    total = 0
    check = 0
    for rnd in range(10):
        for g in range(10):
            hi = next_random()
            at = (hi * 32768 + next_random()) % 100000
            plants[g][at] = next_random() % 10000 + 1
            grows[g][at] = next_random() % 10000 + 1
            day = earliest_full_bloom(plants[g], grows[g])
            total += day
            check = (check * 31 + day + rnd) % 1000000007
    print(f"100 solves: {total} days in all, checksum {check}")


main()
