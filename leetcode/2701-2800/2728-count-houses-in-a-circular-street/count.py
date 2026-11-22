# LeetCode #2728: Count Houses in a Circular Street -- the ★ arm in Python
# (count.kara): every door closed over k moves right, the door here
# opened, and the houses counted moving right until it comes round.


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

    def move_left(self):
        self.at = (self.at - 1) % len(self.doors)
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
    print(house_count(Street([False, False, False, False], 0), 10))
    print(house_count(Street([True, False, True, True, False], 2), 5))
    print(house_count(Street([True], 0), 1))
    print(house_count(Street([True] * 1000, 500), 1000))
    print(house_count(Street([True] * 999, 0), 1000))
    for count, most in [(3000, 12), (300, 1000)]:
        total = 0
        check = 0
        for _ in range(count):
            n = next_random() % most + 1
            k = n + next_random() % (16 - n) if most == 12 else n + next_random() % (1001 - n)
            doors = [next_random() % 2 == 0 for _ in range(n)]
            at = next_random() % n
            a = house_count(Street(doors, at), k)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"{count} streets of up to {most}: houses sum to {total}, checksum {check}")


main()
