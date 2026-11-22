# LeetCode #2833: Furthest Point From Origin -- the bench, mirrored from
# furthest.kara: the L and R counts, and the blanks.


def furthest_distance_from_origin(moves):
    left = moves.count("L")
    right = moves.count("R")
    return abs(left - right) + len(moves) - left - right


seed = 2833


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 100000, 100, 50
    strings = []
    for _ in range(count):
        blank = next_random() % 6
        out = []
        for _ in range(n):
            r = next_random() % 6
            out.append("_" if r < blank else ("L" if r % 2 == 0 else "R"))
        strings.append("".join(out))
    total = 0
    check = 0
    for r in range(rounds):
        for moves in strings:
            d = furthest_distance_from_origin(moves)
            total += d
            check = (check * 31 + d + r) % 1000000007
    print(f"{count} strings of {n}, {rounds} rounds: distances total {total}, checksum {check}")


main()
