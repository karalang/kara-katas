# LeetCode #2139: Minimum Moves to Reach Target Score -- the benchmark, the
# same algorithm as moves.kara.


def min_moves(target, max_doubles):
    doubles = max_doubles
    moves = 0
    while target > 1 and doubles > 0:
        if target % 2 == 1:
            target -= 1
        else:
            target //= 2
            doubles -= 1
        moves += 1
    return moves + target - 1


seed = 2139


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    targets = []
    for _ in range(1000):
        hi = next_random()
        targets.append((hi * 32768 + next_random()) % 1000000000 + 1)
    total = 0
    check = 0
    for r in range(4000):
        for i in range(1000):
            moves = min_moves(targets[i] + r, r % 40)
            total += moves
            check = (check * 31 + moves) % 1000000007
    print(f"4000000 solves: {total} moves in all, checksum {check}")


main()
