# benchmark's Python mirror of collisions.kara (LeetCode #2211, the ★
# arm): skip the leading 'L's and the trailing 'R's and count the cars
# between that are not 'S'.


def count_collisions(directions):
    cars = list(directions)
    lo = 0
    while lo < len(cars) and cars[lo] == "L":
        lo += 1
    hi = len(cars)
    while hi > lo and cars[hi - 1] == "R":
        hi -= 1
    count = 0
    for i in range(lo, hi):
        if cars[i] != "S":
            count += 1
    return count


seed = 2211


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    roads = []
    for r in range(20):
        # a run of left-movers at the front and right-movers at the back,
        # each r thousand cars long, around random cars
        cars = []
        for i in range(100000):
            if i < r * 1000:
                cars.append("L")
            elif i >= 100000 - r * 1000:
                cars.append("R")
            else:
                cars.append("LRS"[next_random() % 3])
        roads.append("".join(cars))
    check = 0
    for p in range(10):
        for road in roads:
            check = (check * 31 + count_collisions(road) + p) % 1000000007
    print(f"10 passes over 20 roads: checksum {check}")


main()
