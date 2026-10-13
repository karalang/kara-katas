# Benchmark for #475: Python mirror of the ★ arm (sort the heaters,
# binary search per house); see heaters.kara.


def first_at_or_after(heaters, x):
    lo = 0
    hi = len(heaters)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if heaters[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def find_radius(houses, heaters):
    ws = sorted(heaters)
    radius = 0
    for house in houses:
        at = first_at_or_after(ws, house)
        nearest = 2**63 - 1
        if at < len(ws):
            nearest = ws[at] - house
        if at > 0 and house - ws[at - 1] < nearest:
            nearest = house - ws[at - 1]
        if nearest > radius:
            radius = nearest
    return radius


seed = 475


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    houses = []
    for _ in range(30000):
        houses.append(1 + (next_random() * 32768 + next_random()) % 1000000000)
    rounds = 200
    total = 0
    checksum = 0
    for _ in range(rounds):
        heaters = []
        for _ in range(30000):
            heaters.append(1 + (next_random() * 32768 + next_random()) % 1000000000)
        got = find_radius(houses, heaters)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{rounds} rounds of 30000 houses and 30000 heaters: radii add up to {total}, checksum {checksum}")


main()
