# LeetCode #2136: Earliest Possible Day of Full Bloom -- the mirror of
# bloom.kara: the seeds sorted by grow time, longest first, and the
# latest of each one's planting finished plus its grow time.


def earliest_full_bloom(plant_time, grow_time):
    order = sorted(range(len(plant_time)), key=lambda i: -grow_time[i])
    planted = 0
    bloom = 0
    for i in order:
        planted += plant_time[i]
        bloom = max(bloom, planted + grow_time[i])
    return bloom


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def text(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(plant_time, grow_time):
    print(f"{text(plant_time)} {text(grow_time)} -> {earliest_full_bloom(plant_time, grow_time)}")


def main():
    show([1, 4, 3], [2, 3, 1])
    show([1, 2, 3, 2], [2, 1, 2, 1])
    show([1], [1])
    show([3, 1, 2], [5, 5, 5])
    show([2, 2, 2], [1, 6, 3])
    show([9, 1], [1, 9])
    show([10000, 10000], [10000, 10000])
    seed = [2136]
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random(seed) % 10 + 1
        top = [3, 10, 100][rnd % 3]
        plant = [next_random(seed) % top + 1 for _ in range(n)]
        grow = [next_random(seed) % top + 1 for _ in range(n)]
        day = earliest_full_bloom(plant, grow)
        total += day
        check = (check * 31 + day + n) % 1000000007
    print(f"2000 gardens: {total} days in all, checksum {check}")
    same = [10000] * 100000
    rising = [i % 10000 + 1 for i in range(100000)]
    falling = [10000 - i % 10000 for i in range(100000)]
    plant = [next_random(seed) % 10000 + 1 for _ in range(100000)]
    grow = [next_random(seed) % 10000 + 1 for _ in range(100000)]
    x = earliest_full_bloom(same, same)
    y = earliest_full_bloom(rising, falling)
    z = earliest_full_bloom(plant, grow)
    print(f"100000 seeds: {x} all largest, {y} rising against falling, {z} at random")


main()
