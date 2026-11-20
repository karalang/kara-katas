# LeetCode #1222: Queens That Can Attack the King -- the Python mirror of
# the ★ arm: mark the queens on an 8 by 8 board, then walk out from the
# king in each of the eight directions; the first queen met in each is one
# that attacks. O(64).

seed = 1222


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def queens_attackthe_king(queens, king):
    board = [[False] * 8 for _ in range(8)]
    for q in queens:
        board[q[0]][q[1]] = True
    attackers = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            x = king[0] + dx
            y = king[1] + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if board[x][y]:
                    attackers.append([x, y])
                    break
                x += dx
                y += dy
    return attackers


def board(count):
    squares = list(range(64))
    for k in range(count + 1):
        j = k + next_random() % (64 - k)
        squares[k], squares[j] = squares[j], squares[k]
    queens = [[s // 8, s % 8] for s in squares[0:count]]
    return queens, [squares[count] // 8, squares[count] % 8]


def main():
    print(sorted(queens_attackthe_king([[0, 1], [1, 0], [4, 0], [0, 4], [3, 3], [2, 4]], [0, 0])))
    print(sorted(queens_attackthe_king([[0, 0], [1, 1], [2, 2], [3, 4], [3, 5], [4, 4], [4, 5]], [3, 3])))
    print(sorted(queens_attackthe_king([[1, 2], [2, 1], [7, 6]], [0, 0])))
    total = 0
    check = 0
    for _ in range(1000):
        count = next_random() % 63 + 1
        queens, king = board(count)
        attackers = sorted(queens_attackthe_king(queens, king))
        total += len(attackers)
        for a in attackers:
            check = (check * 131 + a[0] * 8 + a[1] + 1) % 1000000007
        check = (check * 131 + 99) % 1000000007
    print(f"1000 boards of 1 to 63 queens: attackers total {total}, checksum {check}")
    for king in [[0, 0], [3, 4], [7, 2]]:
        queens = [[s // 8, s % 8] for s in range(64) if s != king[0] * 8 + king[1]]
        print(f"63 queens, king at {king}: {sorted(queens_attackthe_king(queens, king))}")


main()
