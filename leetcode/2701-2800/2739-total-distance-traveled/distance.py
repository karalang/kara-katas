# LeetCode #2739: Total Distance Traveled -- Python mirror of
# distance.kara (the ★ arm): (m - 1) // 4 transfers, as many as the
# additional tank holds, and 10 km a liter.


def distance_traveled(main_tank, additional_tank):
    transfers = min((main_tank - 1) // 4, additional_tank)
    return (main_tank + transfers) * 10


def main():
    print(distance_traveled(5, 10))
    print(distance_traveled(1, 2))
    print(distance_traveled(1, 1))
    print(distance_traveled(4, 100))
    print(distance_traveled(5, 1))
    print(distance_traveled(9, 2))
    print(distance_traveled(100, 100))
    total = check = 0
    for main_tank in range(1, 101):
        for additional_tank in range(1, 101):
            d = distance_traveled(main_tank, additional_tank)
            total += d
            check = (check * 31 + d) % 1000000007
    print(f"10000 pairs of tanks: distances sum to {total}, checksum {check}")


main()
