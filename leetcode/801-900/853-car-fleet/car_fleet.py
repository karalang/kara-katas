# LeetCode #853: Car Fleet -- Python mirror of the ★ arm and its harness.


def car_fleet(target, position, speed):
    cars = sorted(zip(position, speed))
    fleets = 0
    far = 0
    fast = 1
    for p, s in reversed(cars):
        if (target - p) * fast > far * s:
            fleets += 1
            far = target - p
            fast = s
    return fleets


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(target, position, speed):
    print(f"{target}, {fmt(position)}, {fmt(speed)} -> {car_fleet(target, position, speed)}")


seed = 853


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def positions(n, target):
    out = []
    taken = [False] * target
    while len(out) < n:
        p = (next_random() * 32768 + next_random()) % target
        if not taken[p]:
            taken[p] = True
            out.append(p)
    return out


def main():
    show(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3])
    show(10, [3], [3])
    show(100, [0, 2, 4], [4, 2, 1])
    show(10, [0, 4, 2], [2, 1, 3])
    show(10, [6, 8], [3, 2])
    show(10, [0, 5], [2, 1])
    show(10, [0, 5], [1, 2])
    show(10, [9, 8, 7, 6], [1, 1, 1, 1])
    show(10, [9, 8, 7, 6], [1, 2, 3, 4])
    show(20, [6, 2, 17], [3, 9, 2])
    show(1000000, [0, 999999], [1000000, 1])
    n = 100000
    target = 1000000
    same = [7] * n
    slower = [n - i for i in range(n)]
    lined = [i * 10 for i in range(n)]
    print(f"10^5 cars at one speed: {car_fleet(target, lined, same)}")
    print(f"10^5 cars, each faster than the one ahead: {car_fleet(target, lined, slower)}")
    random_speed = [1 + (next_random() * 32768 + next_random()) % 1000000 for _ in range(n)]
    print(f"10^5 cars at random places and speeds: {car_fleet(target, positions(n, target), random_speed)}")
    total = 0
    check = 0
    for _ in range(600):
        target = 1 + next_random() % 30
        n = 1 + next_random() % target
        place = positions(min(n, 12), target)
        speed = [1 + next_random() % 6 for _ in range(len(place))]
        fleets = car_fleet(target, place, speed)
        total += fleets
        check = (check * 31 + fleets) % 1000000007
    print(f"600 random roads: fleets sum to {total}, checksum {check}")


main()
