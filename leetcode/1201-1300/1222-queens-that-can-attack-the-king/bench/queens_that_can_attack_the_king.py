# LeetCode #1222 bench, Python mirror of the Kāra ★ arm: mark the queens on
# an 8 by 8 board, then walk out from the king in each of the eight
# directions, over 5000 random boards of 1 to 63 queens drawn once, 50
# passes; checksum of the attackers in the order found.

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


def main():
    boards = []
    for _ in range(5000):
        count = next_random() % 63 + 1
        squares = list(range(64))
        for k in range(count + 1):
            j = k + next_random() % (64 - k)
            squares[k], squares[j] = squares[j], squares[k]
        queens = [[s // 8, s % 8] for s in squares[0:count]]
        boards.append((queens, [squares[count] // 8, squares[count] % 8]))
    total = 0
    check = 0
    for _ in range(200):
        for queens, king in boards:
            attackers = queens_attackthe_king(queens, king)
            total += len(attackers)
            for a in attackers:
                check = (check * 131 + a[0] * 8 + a[1] + 1) % 1000000007
    print(f"5000 boards of 1 to 63 queens, 200 passes: attackers total {total}, checksum {check}")


main()
