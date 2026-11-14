# LeetCode #2147: Number of Ways to Divide a Long Corridor -- the
# benchmark's Python mirror of corridor.kara.

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


def main():
    corridors = []
    for _ in range(4):
        corridor = "".join("S" if next_random() % 3 == 0 else "P" for _ in range(99999))
        corridor += "S" if corridor.count("S") % 2 == 1 else "P"
        corridors.append(corridor)
    total = 0
    check = 0
    for rnd in range(25):
        for c in range(4):
            i = next_random() % 99999
            place = corridors[c]
            corridors[c] = place[:i] + place[i + 1:i + 2] + place[i:i + 1] + place[i + 2:]
            ways = number_of_ways(corridors[c])
            total = (total + ways) % MOD
            check = (check * 31 + ways + rnd) % MOD
    print(f"100 counts: {total} ways in all, checksum {check}")


main()
