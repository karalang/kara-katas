# LeetCode #475: Heaters -- Python mirror of the ★ arm (heaters.kara):
# sort the heaters, binary search per house.


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


# ---- test harness ---------------------------------------------------------

def show(houses, heaters):
    a = ", ".join(str(x) for x in houses)
    b = ", ".join(str(x) for x in heaters)
    print(f"houses [{a}], heaters [{b}] -> {find_radius(houses, heaters)}")


seed = 475


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([1, 2, 3], [2])
    show([1, 2, 3, 4], [1, 4])
    show([1, 5], [2])
    show([7], [7])
    show([1, 1000000000], [1, 1000000000])
    show([1, 1000000000], [500000000])
    show([5, 4, 3, 2, 1], [10, 9, 8])
    show([3, 3, 3], [1, 5, 1, 5])
    show([1, 2, 3, 5, 15], [2, 30])
    count = 300
    total = 0
    checksum = 0
    for c in range(count):
        span = 1000000000 if c % 10 == 9 else 100
        houses = []
        for _ in range(1 + next_random() % 30):
            houses.append(1 + (next_random() * 32768 + next_random()) % span)
        heaters = []
        for _ in range(1 + next_random() % 10):
            heaters.append(1 + (next_random() * 32768 + next_random()) % span)
        got = find_radius(houses, heaters)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} random cases: radii add up to {total}, checksum {checksum}")


main()
