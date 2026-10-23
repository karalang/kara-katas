# LeetCode #887: Super Egg Drop -- Python mirror of the floors-per-moves
# solution in super_egg_drop.kara, with the same test harness.
#
# Turn the question round: with m moves and k eggs, how many floors can
# be told apart? The first drop goes from some floor; if the egg breaks,
# m - 1 moves and k - 1 eggs settle the floors below it, and if not, m -
# 1 moves and k eggs settle those above. So floors(m, k) = floors(m - 1,
# k - 1) + floors(m - 1, k) + 1, and the answer is the least m with
# floors(m, k) >= n. One row per move, k entries each. O(k * answer).


def super_egg_drop(k, n):
    floors = [0] * (k + 1)
    moves = 0
    while floors[k] < n:
        moves += 1
        for eggs in range(k, 0, -1):
            floors[eggs] = floors[eggs - 1] + floors[eggs] + 1
    return moves


# ---- test harness ----------------------------------------------------------


def show(k, n):
    print(f"k = {k}, n = {n} -> {super_egg_drop(k, n)}")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    show(1, 2)
    show(2, 6)
    show(3, 14)
    show(1, 1)
    show(1, 10000)
    show(2, 10000)
    show(3, 10000)
    show(100, 10000)
    show(14, 10000)
    show(13, 8191)
    show(13, 8192)
    # small cases
    seed = 887
    total = 0
    for _ in range(3000):
        k = next_random() % 5 + 1
        n = next_random() % 80 + 1
        total += super_egg_drop(k, n)
    print(f"3000 cases of up to 5 eggs and 80 floors: {total} moves")
    # LeetCode's sizes, with up to 12 eggs
    total = 0
    check = 0
    for _ in range(20):
        k = next_random() % 12 + 1
        n = next_random() % 10000 + 1
        moves = super_egg_drop(k, n)
        total += moves
        check = (check * 131 + moves) % 1000000007
    print(f"20 cases of up to 12 eggs and 10000 floors: {total} moves, checksum {check}")


main()
