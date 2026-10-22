# Benchmark for #853: Car Fleet -- Python twin of the Kāra ★ arm (closest
# to the target first).


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


seed = 853


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 150
    n = 100000
    target = 1000000
    positions = []
    speeds = []
    for g in range(count):
        top = 1 + (g % 8) * 142857
        taken = [False] * target
        position = []
        while len(position) < n:
            p = (next_random() * 32768 + next_random()) % target
            if not taken[p]:
                taken[p] = True
                position.append(p)
        speed = [1 + (next_random() * 32768 + next_random()) % top for _ in range(n)]
        positions.append(position)
        speeds.append(speed)
    total = 0
    checksum = 0
    for round_ in range(rounds):
        g = round_ % count
        f = car_fleet(target, positions[g], speeds[g])
        total += f
        checksum = (checksum * 31 + f) % 1000000007
    print(f"{rounds} rounds of {count} roads: fleets sum to {total}, checksum {checksum}")


main()
