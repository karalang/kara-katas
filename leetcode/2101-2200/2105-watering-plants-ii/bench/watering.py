# LeetCode #2105: Watering Plants II -- bench, Python mirror of
# watering.kara.


def minimum_refill(plants, capacity_a, capacity_b):
    i, j = 0, len(plants) - 1
    a, b = capacity_a, capacity_b
    refills = 0
    while i < j:
        if a < plants[i]:
            refills += 1
            a = capacity_a
        a -= plants[i]
        if b < plants[j]:
            refills += 1
            b = capacity_b
        b -= plants[j]
        i += 1
        j -= 1
    if i == j and max(a, b) < plants[i]:
        refills += 1
    return refills


seed = 2105


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


rows = []
for _ in range(200):
    plants = [wide_random() % 1000000 + 1 for _ in range(100000)]
    most = max(plants)
    a = most + wide_random() % (2000000 - most + 1)
    b = most + wide_random() % (2000000 - most + 1)
    rows.append((plants, a, b))
total = 0
check = 0
for _ in range(10):
    for plants, a, b in rows:
        got = minimum_refill(plants, a, b)
        total += got
        check = (check * 31 + got) % 1000000007
print(f"2000 rows: {total} refills, checksum {check}")
