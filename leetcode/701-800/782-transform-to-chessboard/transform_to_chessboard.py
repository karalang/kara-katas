# LeetCode 782 — Transform to Chessboard, the corner rule and two counts.
# Mirrors transform_to_chessboard.kara (the ★ arm) and its harness.


def moves_to_chessboard(board):
    n = len(board)
    for r in range(n):
        for c in range(n):
            if board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c] == 1:
                return -1
    row_ones = col_ones = row_off = col_off = 0
    for i in range(n):
        row_ones += board[0][i]
        col_ones += board[i][0]
        if board[i][0] == i % 2:
            row_off += 1
        if board[0][i] == i % 2:
            col_off += 1
    if row_ones != n // 2 and row_ones != (n + 1) // 2:
        return -1
    if col_ones != n // 2 and col_ones != (n + 1) // 2:
        return -1
    if n % 2 == 1:
        if row_off % 2 == 1:
            row_off = n - row_off
        if col_off % 2 == 1:
            col_off = n - col_off
    else:
        row_off = min(row_off, n - row_off)
        col_off = min(col_off, n - col_off)
    return (row_off + col_off) // 2


seed = 782


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled_chessboard(n):
    row_of = list(range(n))
    col_of = list(range(n))
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        row_of[i], row_of[j] = row_of[j], row_of[i]
        j = next_random() % (i + 1)
        col_of[i], col_of[j] = col_of[j], col_of[i]
        i -= 1
    return [[(row_of[r] + col_of[c]) % 2 for c in range(n)] for r in range(n)]


def show(board):
    print(f"{board} -> {moves_to_chessboard(board)}")


def main():
    show([[0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1]])
    show([[0, 1], [1, 0]])
    show([[1, 0], [1, 0]])
    show([[0]])
    show([[1, 1, 0], [0, 0, 1], [0, 0, 1]])
    show([[1, 0, 1], [0, 1, 0], [0, 1, 0]])
    show([[1, 1, 0, 0], [0, 0, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1]])
    show([[0, 1, 0, 1], [1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]])
    big = shuffled_chessboard(30)
    print(f"shuffled 30 x 30 -> {moves_to_chessboard(big)}")
    broken = [row[:] for row in big]
    broken[17][11] = 1 - broken[17][11]
    print(f"shuffled 30 x 30, one cell flipped -> {moves_to_chessboard(broken)}")
    print(f"shuffled 29 x 29 -> {moves_to_chessboard(shuffled_chessboard(29))}")
    solvable = moves = check = 0
    for case in range(300):
        n = 1 + next_random() % 12
        board = shuffled_chessboard(n)
        if case % 3 == 1:
            r = next_random() % n
            c = next_random() % n
            board[r][c] = 1 - board[r][c]
        elif case % 3 == 2:
            for r in range(1, n):
                if next_random() % 2 == 0:
                    board[r] = [1 - v for v in board[0]]
                else:
                    board[r] = board[0][:]
        answer = moves_to_chessboard(board)
        if answer >= 0:
            solvable += 1
            moves += answer
        check = (check * 31 + answer + 2) % 1000000007
    print(f"300 random boards: {solvable} solvable in {moves} moves, checksum {check}")


main()
