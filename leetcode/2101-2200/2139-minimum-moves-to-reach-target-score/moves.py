# LeetCode #2139: Minimum Moves to Reach Target Score -- the Python mirror
# of moves.kara's ★ arm.


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


def show(target, max_doubles):
    print(f"{target} {max_doubles} -> {min_moves(target, max_doubles)}")


def main():
    show(5, 0)
    show(19, 2)
    show(10, 4)
    show(1, 0)
    show(1, 100)
    show(1000000000, 0)
    show(1000000000, 100)
    show(536870912, 29)
    total = 0
    check = 0
    for rnd in range(2000):
        top = [100, 10000, 1000000000][rnd % 3]
        hi = next_random()
        target = (hi * 32768 + next_random()) % top + 1
        doubles = next_random() % [11, 101][rnd % 2]
        moves = min_moves(target, doubles)
        total += moves
        check = (check * 31 + moves + doubles) % 1000000007
    print(f"2000 targets: {total} moves in all, checksum {check}")


main()
