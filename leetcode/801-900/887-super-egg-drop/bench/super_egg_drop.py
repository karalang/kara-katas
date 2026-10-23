# LeetCode #887 bench: the floors a number of moves can cover, on 30000
# cases of 2 to 9 eggs and up to 10^9 floors. The same algorithm as
# super_egg_drop.kara.


def super_egg_drop(k, n):
    floors = [0] * (k + 1)
    moves = 0
    while floors[k] < n:
        moves += 1
        for eggs in range(k, 0, -1):
            floors[eggs] = floors[eggs - 1] + floors[eggs] + 1
    return moves


seed = 887


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    total = 0
    check = 0
    for _ in range(30000):
        k = 2 + next_random() % 8
        hi = next_random()
        n = 1 + (hi * 32768 + next_random()) % 1000000000
        moves = super_egg_drop(k, n)
        total += moves
        check = (check * 131 + moves) % 1000000007
    print(f"30000 cases of 2 to 9 eggs and up to 10^9 floors: {total} moves, checksum {check}")


main()
