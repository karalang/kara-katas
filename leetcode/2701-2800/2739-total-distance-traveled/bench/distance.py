# LeetCode #2739: Total Distance Traveled -- the bench (distance.kara in
# Python): (m - 1) // 4 transfers, as many as the additional tank holds.


def distance_traveled(main_tank, additional_tank):
    transfers = min((main_tank - 1) // 4, additional_tank)
    return (main_tank + transfers) * 10


def main():
    count, rounds = 1000000, 100
    seed = 2739
    tanks = []
    for _ in range(count):
        seed = (seed * 1103515245 + 12345) % 2147483648
        m = seed // 65536 % 100 + 1
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = seed // 65536 % 100 + 1
        tanks.append((m, a))
    total = check = 0
    for r in range(rounds):
        for m, a in tanks:
            d = distance_traveled(m, a)
            total += d
            check = (check * 31 + d + r) % 1000000007
    print(f"{count} pairs of tanks, {rounds} rounds: distances sum to {total}, checksum {check}")


main()
