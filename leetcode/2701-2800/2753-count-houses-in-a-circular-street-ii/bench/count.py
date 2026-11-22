# LeetCode #2753: Count Houses in a Circular Street II -- the bench in
# Python: the ★ arm over 30 streets of up to 10^5 houses with k = 10^5,
# all drawn first, then each walked 20 times, every walk on a fresh copy
# of its street, the walk closing the doors it meets.


class Street:
    def __init__(self, doors, at):
        self.doors = doors
        self.at = at
        self.moves = 0

    def close_door(self):
        self.doors[self.at] = False

    def is_door_open(self):
        return self.doors[self.at]

    def move_right(self):
        self.at = (self.at + 1) % len(self.doors)
        self.moves += 1


def house_count(street, k):
    while not street.is_door_open():
        street.move_right()
    last = 0
    for step in range(1, k + 1):
        street.move_right()
        if street.is_door_open():
            street.close_door()
            last = step
    return last


seed = 2753


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 30
    rounds = 20
    k = 100000
    cases = []
    for _ in range(count):
        n = next_random() % k + 1
        doors = [next_random() % 2 == 0 for _ in range(n)]
        doors[next_random() % n] = True
        cases.append((doors, next_random() % n))
    total = 0
    moves = 0
    check = 0
    for r in range(rounds):
        for doors, at in cases:
            street = Street(list(doors), at)
            a = house_count(street, k)
            total += a
            moves += street.moves
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} streets, {rounds} rounds: houses sum to {total} in {moves} moves, checksum {check}")


main()
