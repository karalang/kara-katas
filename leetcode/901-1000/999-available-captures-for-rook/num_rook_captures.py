# LeetCode #999: Available Captures for Rook -- mirror of the ★ arm
# (num_rook_captures.kara), a walk from the rook in each direction.


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


def parse(rows):
    return [list(row) for row in rows]


# a board with the rook on a random square and each other square a pawn
# `pawns` times in 16 and a bishop `bishops` times in 16
def random_board(pawns, bishops):
    rook = next_random() % 64
    board = []
    for r in range(8):
        row = []
        for c in range(8):
            if r * 8 + c == rook:
                row.append("R")
            else:
                x = next_random() % 16
                if x < pawns:
                    row.append("p")
                elif x < pawns + bishops:
                    row.append("B")
                else:
                    row.append(".")
        board.append(row)
    return board


def text(board):
    return "/".join("".join(row) for row in board)


def main():
    examples = [
        ["........", "...p....", "...R...p", "........",
         "........", "...p....", "........", "........"],
        ["........", ".ppppp..", ".ppBpp..", ".pBRBp..",
         ".ppBpp..", ".ppppp..", "........", "........"],
        ["........", "...p....", "...p....", "pp.R.pB.",
         "........", "...B....", "...p....", "........"],
        ["R.......", "........", "........", "........",
         "........", "........", "........", "........"],
        ["pppppppp", "pppppppp", "pppppppp", "pppRpppp",
         "pppppppp", "pppppppp", "pppppppp", "pppppppp"],
        ["Rppppppp", "pppppppp", "pppppppp", "pppppppp",
         "pppppppp", "pppppppp", "pppppppp", "pppppppp"],
        ["p......p", "........", "........", "........",
         "........", "........", "........", "p......R"],
        ["...p....", "...B....", "........", "pB.R..Bp",
         "........", "........", "...B....", "...p...."],
        ["........", "........", "...p....", "..pRp...",
         "...p....", "........", "........", "........"],
        ["BBBBBBBB", "BBBBBBBB", "BBBBBBBB", "BBBRBBBB",
         "BBBBBBBB", "BBBBBBBB", "BBBBBBBB", "BBBBBBBB"],
    ]
    for rows in examples:
        print(f"{'/'.join(rows)} -> {num_rook_captures(parse(rows))}")
    every = 0
    for square in range(64):
        rows = []
        for r in range(8):
            rows.append("".join("R" if r * 8 + c == square else "p" for c in range(8)))
        every += num_rook_captures(parse(rows))
    print(f"the rook on each of the 64 squares of a board of pawns: {every} captures")
    for count, pawns, bishops in [(300, 1, 1), (3000, 3, 2), (3000, 6, 4)]:
        npawns = 0
        captures = 0
        check = 0
        for _ in range(count):
            board = random_board(pawns, bishops)
            got = num_rook_captures(board)
            npawns += sum(row.count("p") for row in board)
            captures += got
            check = (check * 31 + got + 1) % 1000000007
        print(f"{count} random boards with {npawns} pawns: {captures} captures, checksum {check}")


main()
