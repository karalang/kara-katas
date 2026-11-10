# LeetCode #1103: Distribute Candies to People -- Python mirror of the ★
# arm: gifts of 1, 2, 3, ... candies to each person in turn, round and
# round, the last gift whatever is left. Same cases and output as
# distribute_candies.kara.


def distribute_candies(candies, num_people):
    people = [0] * num_people
    left = candies
    gift = 1
    while left > 0:
        given = min(gift, left)
        people[(gift - 1) % num_people] += given
        left -= given
        gift += 1
    return people


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(people):
    check = 0
    for c in people:
        check = (check * 31 + c + 1) % 1000000007
    return check


def main():
    global seed
    cases = [(7, 4), (10, 3), (1, 1), (1, 5), (6, 3), (7, 3), (21, 6), (22, 6), (100, 1), (55, 10), (60, 10)]
    for candies, n in cases:
        people = distribute_candies(candies, n)
        print(f"{candies} to {n}: [{','.join(str(c) for c in people)}]")
    seed = 1103
    check = 0
    for _ in range(2000):
        hi = next_random()
        candies = (hi * 32768 + next_random()) % 1000000 + 1
        n = next_random() % 1000 + 1
        check = (check * 31 + fold(distribute_candies(candies, n))) % 1000000007
    print(f"2000 random problems: checksum {check}")
    for n in [1, 2, 999, 1000]:
        people = distribute_candies(1000000000, n)
        print(f"10^9 to {n}: first {people[0]}, last {people[n - 1]}, checksum {fold(people)}")


main()
