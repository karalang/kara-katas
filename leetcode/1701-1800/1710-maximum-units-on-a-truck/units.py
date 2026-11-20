# LeetCode #1710: Maximum Units on a Truck -- the Python mirror of the ★
# arm (units.kara): the box types sorted by units, most first, and boxes
# taken from the front until the truck is full.


def maximum_units(box_types, truck_size):
    order = sorted(box_types, key=lambda t: -t[1])
    room = truck_size
    total = 0
    for boxes, units in order:
        take = min(boxes, room)
        total += take * units
        room -= take
        if room == 0:
            break
    return total


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, boxes, units, truck, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        box_types = []
        for _ in range(n):
            b = next_random(seed) % boxes + 1
            u = next_random(seed) % units + 1
            box_types.append([b, u])
        a = next_random(seed)
        size = (a * 32768 + next_random(seed)) % truck + 1
        answer = maximum_units(box_types, size)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} problems of up to {most} box types: answers sum to {total}, checksum {check}")


def main():
    # LeetCode's two examples, then a truck bigger than every box, one
    # box, and two types of the same units
    print(maximum_units([[1, 3], [2, 2], [3, 1]], 4))
    print(maximum_units([[5, 10], [2, 5], [4, 7], [3, 9]], 10))
    print(maximum_units([[2, 7], [3, 4]], 100))
    print(maximum_units([[1, 1]], 1))
    print(maximum_units([[3, 5], [4, 5], [1, 9]], 6))
    seed = [1710]
    batch(3000, 6, 5, 5, 20, seed)
    batch(300, 1000, 1000, 1000, 1000000, seed)
    batch(10, 1000, 1000, 1000, 1000, seed)


main()
