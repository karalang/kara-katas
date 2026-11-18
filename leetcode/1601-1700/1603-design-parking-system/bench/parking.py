# LeetCode #1603: Design Parking System -- the bench in Python, mirroring
# parking.kara: the spaces left of each size in a list.


class ParkingSystem:
    def __init__(self, big, medium, small):
        self.left = [big, medium, small]

    def add_car(self, car_type):
        slot = car_type - 1
        if self.left[slot] == 0:
            return False
        self.left[slot] -= 1
        return True


def main():
    seed = 1603

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    lots = []
    for _ in range(1000):
        big = next_random() % 3001
        medium = next_random() % 3001
        small = next_random() % 3001
        lots.append((big, medium, small))
    cars = [next_random() % 3 + 1 for _ in range(10000000)]
    check = parked = 0
    for rnd in range(20):
        for k, (big, medium, small) in enumerate(lots):
            lot = ParkingSystem(big, medium, small)
            count = 0
            for c in cars[k * 10000:(k + 1) * 10000]:
                if lot.add_car(c):
                    count += 1
            parked += count
            check = (check * 31 + count + rnd + 1) % 1000000007
    print(f"20 rounds of 1000 lots of up to 3000 spaces a size, 10000 cars each: {parked} parked, checksum {check}")


main()
