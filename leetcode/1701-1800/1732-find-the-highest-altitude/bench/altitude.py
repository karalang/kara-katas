# LeetCode #1732: Find the Highest Altitude -- the bench (altitude.kara):
# the altitudes listed, then the largest.


def largest_altitude(gain):
    altitudes = [0]
    for g in gain:
        altitudes.append(altitudes[-1] + g)
    return max(altitudes)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 1000
    rounds = 2000
    n = 100
    seed = [1732]
    trips = []
    for _ in range(count):
        trips.append([next_random(seed) % 201 - 100 for _ in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for gain in trips:
            answer = largest_altitude(gain)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} trips of {n} gains, {rounds} rounds: highest points sum to {total}, checksum {check}")


main()
