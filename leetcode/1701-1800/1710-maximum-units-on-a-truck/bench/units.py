# LeetCode #1710: Maximum Units on a Truck -- the Python mirror of the
# bench (units.kara): the box types sorted by units, most first, and
# boxes taken from the front until the truck is full, on 1000 random
# problems of 1000 box types, each answered 10 times.


def maximum_units(box_types, truck_size):
    order = sorted((list(t) for t in box_types), key=lambda t: -t[1])
    room = truck_size
    total = 0
    for t in order:
        take = min(t[0], room)
        total += take * t[1]
        room -= take
        if room == 0:
            break
    return total


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count = 1000
    rounds = 10
    n = 1000
    seed = [1710]
    problems = []
    for _ in range(count):
        box_types = []
        for _ in range(n):
            b = next_random(seed) % 1000 + 1
            u = next_random(seed) % 1000 + 1
            box_types.append([b, u])
        a = next_random(seed)
        size = (a * 32768 + next_random(seed)) % 1000000 + 1
        problems.append((box_types, size))
    total = 0
    check = 0
    for r in range(rounds):
        for box_types, size in problems:
            answer = maximum_units(box_types, size)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {n} box types, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
