# Benchmark for #782: Transform to Chessboard -- mirror of the ★ arm (the
# corner rule and two counts), with the same workload as the Kāra program.


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


def main():
    count, n = 64, 30
    boards = []
    for g in range(count):
        row_of = list(range(n))
        col_of = list(range(n))
        i = n - 1
        while i > 0:
            j = next_random() % (i + 1)
            row_of[i], row_of[j] = row_of[j], row_of[i]
            j = next_random() % (i + 1)
            col_of[i], col_of[j] = col_of[j], col_of[i]
            i -= 1
        board = [[(row_of[r] + col_of[c]) % 2 for c in range(n)] for r in range(n)]
        if g % 4 == 1:
            r = next_random() % n
            c = next_random() % n
            board[r][c] = 1 - board[r][c]
        elif g % 4 == 3:
            board[0] = [next_random() % 2 for _ in range(n)]
            for r in range(1, n):
                flip = next_random() % 2
                board[r] = [v ^ flip for v in board[0]]
        boards.append(board)
    solvable = 0
    checksum = 0
    for rnd in range(2000000):
        g = (rnd * 7) % count
        answer = moves_to_chessboard(boards[g])
        if answer >= 0:
            solvable += 1
        checksum = (checksum * 31 + answer + 2 + g) % 1000000007
    print(f"2000000 rounds of 30 x 30 boards: {solvable} solvable, checksum {checksum}")


main()
