# LeetCode #2728: Count Houses in a Circular Street -- the bench in
# Python: the ★ arm over 300 streets of up to 1000 houses with k = 1000,
# all drawn first, then each walked 500 times through the judge's
# street, whose moves are counted.


class Street:
    def __init__(self, doors, at):
        self.doors = doors
        self.at = at
        self.moves = 0

    def open_door(self):
        self.doors[self.at] = True

    def close_door(self):
        self.doors[self.at] = False

    def is_door_open(self):
        return self.doors[self.at]

    def move_right(self):
        self.at = (self.at + 1) % len(self.doors)
        self.moves += 1


def house_count(street, k):
    for _ in range(k):
        street.close_door()
        street.move_right()
    street.open_door()
    houses = 1
    street.move_right()
    while not street.is_door_open():
        houses += 1
        street.move_right()
    return houses


seed = 2728


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 300
    rounds = 500
    streets = []
    for _ in range(count):
        n = next_random() % 1000 + 1
        doors = [next_random() % 2 == 0 for _ in range(n)]
        streets.append(Street(doors, next_random() % n))
    total = 0
    check = 0
    for r in range(rounds):
        for street in streets:
            a = house_count(street, 1000)
            total += a
            check = (check * 31 + a + r) % 1000000007
    moves = sum(s.moves for s in streets)
    print(f"{count} streets, {rounds} rounds: houses sum to {total} in {moves} moves, checksum {check}")


main()
