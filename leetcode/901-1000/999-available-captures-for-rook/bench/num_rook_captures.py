# Benchmark: LeetCode #999 Available Captures for Rook -- the ★ arm, a
# walk from the rook each way, on random 8 by 8 boards. Mirrors
# num_rook_captures.kara, .c, .rs and go-seq/.


def num_rook_captures(board):
    rr = 0
    rc = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == "R":
                rr = r
                rc = c
    captures = 0
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r = rr + dr
        c = rc + dc
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "p":
                captures += 1
                break
            if board[r][c] == "B":
                break
            r += dr
            c += dc
    return captures


seed = 999


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 500000
    # 20 boards, the rook on a random square and each other square a pawn
    # 4 times in 16 and a bishop 2 times in 16
    boards = []
    for _ in range(20):
        rook = next_random() % 64
        board = []
        for r in range(8):
            row = []
            for c in range(8):
                x = next_random() % 16
                if r * 8 + c == rook:
                    row.append("R")
                elif x < 4:
                    row.append("p")
                elif x < 6:
                    row.append("B")
                else:
                    row.append(".")
            board.append(row)
        boards.append(board)
    captures = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            k = (r + i) % 20
            got = num_rook_captures(boards[k])
            captures += got
            check = (check * 31 + got + 1) % 1000000007
            # a pawn put on or taken off one square, so no board stays put
            s = (r * 13 + i * 5) % 64
            row = boards[k][s // 8]
            if row[s % 8] == ".":
                row[s % 8] = "p"
            elif row[s % 8] == "p":
                row[s % 8] = "."
    print(f"{rounds} rounds over 20 boards: {captures} captures, checksum {check}")


main()
