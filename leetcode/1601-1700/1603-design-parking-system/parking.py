# LeetCode #1603: Design Parking System -- the Python mirror of
# parking.kara (the ★ arm): the spaces left of each size in a list. Its
# output is byte-identical to the Kāra arms'.


class ParkingSystem:
    def __init__(self, big, medium, small):
        self.left = [big, medium, small]

    def add_car(self, car_type):
        slot = car_type - 1
        if self.left[slot] == 0:
            return False
        self.left[slot] -= 1
        return True


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, cars, rng):
    check = parked = 0
    for _ in range(count):
        big = rng.next() % (most + 1)
        medium = rng.next() % (most + 1)
        small = rng.next() % (most + 1)
        lot = ParkingSystem(big, medium, small)
        for _ in range(cars):
            ok = lot.add_car(rng.next() % 3 + 1)
            if ok:
                parked += 1
            check = mix(check, 1 if ok else 0)
    print(f"{count} lots of up to {most} spaces a size, {count * cars} cars: {parked} parked, checksum {check}")


def main():
    examples = [((1, 1, 0), [1, 2, 3, 1]), ((0, 0, 0), [1, 2, 3]), ((2, 2, 2), [3, 3, 3, 2, 1, 2, 1, 1, 2])]
    for (big, medium, small), cars in examples:
        lot = ParkingSystem(big, medium, small)
        answers = ["true" if lot.add_car(c) else "false" for c in cars]
        print(f"[null, {', '.join(answers)}]")
    rng = Rng(1603)
    batch(3000, 3, 10, rng)
    batch(300, 1000, 3000, rng)
    batch(3, 1000, 1000000, rng)


main()
