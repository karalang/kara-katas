# LeetCode #2753: Count Houses in a Circular Street II -- the ★ arm in
# Python (count.kara): to the first open door, then k houses on, each
# open door met closed and its distance kept; the last is the count.


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

    def move_left(self):
        self.at = (self.at - 1) % len(self.doors)
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


def doors(n):
    d = [next_random() % 2 == 0 for _ in range(n)]
    d[next_random() % n] = True
    return d


def main():
    print(house_count(Street([True] * 5, 0), 5))
    print(house_count(Street([True, False, True, False], 1), 7))
    print(house_count(Street([True], 0), 1))
    n = 100000
    print(house_count(Street([True] * n, 777), n))
    one = [False] * n
    one[n - 1] = True
    print(house_count(Street(one, 0), n))
    for count, most in [(3000, 12), (30, 100000)]:
        total = 0
        check = 0
        for _ in range(count):
            m = next_random() % most + 1
            top = 15 if most == 12 else most
            k = m + next_random() % (top + 1 - m)
            d = doors(m)
            at = next_random() % m
            a = house_count(Street(d, at), k)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"{count} streets of up to {most}: houses sum to {total}, checksum {check}")


main()
