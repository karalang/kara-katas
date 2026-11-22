# LeetCode #2833: Furthest Point From Origin -- the Python mirror of the
# ★ arm: the gap between the L and R counts plus every blank.


def furthest_distance_from_origin(moves):
    left = moves.count("L")
    right = moves.count("R")
    return abs(left - right) + len(moves) - left - right


# ---- the harness: the same in every arm --------------------------------

seed = 2833


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def moves_of(n, blank):
    out = []
    for _ in range(n):
        r = next_random() % 6
        out.append("_" if r < blank else ("L" if r % 2 == 0 else "R"))
    return "".join(out)


def main():
    print(furthest_distance_from_origin("L_RL__R"))
    print(furthest_distance_from_origin("_R__LL_"))
    print(furthest_distance_from_origin("_______"))
    print(f"{furthest_distance_from_origin('L')} {furthest_distance_from_origin('R')} {furthest_distance_from_origin('_')}")
    print(f"{furthest_distance_from_origin('LR' * 25)} {furthest_distance_from_origin('L' * 50)}")
    check = 0
    total = 0
    for _ in range(20000):
        n = next_random() % 50 + 1
        blank = next_random() % 6
        d = furthest_distance_from_origin(moves_of(n, blank))
        total += d
        check = (check * 31 + d) % 1000000007
    print(f"20000 random strings: distances total {total}, checksum {check}")


main()
