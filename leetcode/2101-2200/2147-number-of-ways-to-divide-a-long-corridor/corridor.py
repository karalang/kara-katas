# LeetCode #2147: Number of Ways to Divide a Long Corridor -- the Python
# mirror of corridor.kara's ★ arm.

MOD = 1000000007


def number_of_ways(corridor):
    seats = [i for i, ch in enumerate(corridor) if ch == "S"]
    if len(seats) == 0 or len(seats) % 2 == 1:
        return 0
    ways = 1
    for p in range(2, len(seats), 2):
        ways = ways * (seats[p] - seats[p - 1]) % MOD
    return ways


seed = 2147


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(corridor):
    print(f"{corridor} -> {number_of_ways(corridor)}")


def main():
    show("SSPPSPS")
    show("PPSPSP")
    show("S")
    show("PPPP")
    show("SS")
    show("SSPSSPPSS")
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 20 + 1
        one_in = [2, 3, 6][rnd % 3]
        corridor = "".join("S" if next_random() % one_in == 0 else "P" for _ in range(n))
        ways = number_of_ways(corridor)
        total += ways
        check = (check * 31 + ways + n) % 1000000007
    print(f"2000 corridors: {total} ways in all, checksum {check}")
    seats = "S" * 100000
    spaced = "SPSP" * 25000
    rand = "".join("S" if next_random() % 4 == 0 else "P" for _ in range(99999))
    rand += "S" if rand.count("S") % 2 == 1 else "P"
    print(f"100000 places: {number_of_ways(seats)} all seats, {number_of_ways(spaced)} spaced, {number_of_ways(rand)} at random")


main()
