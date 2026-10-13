# LeetCode #529: Minesweeper -- Python mirror of the ★ arm (reveal
# recursively); see update_board.kara. Same algorithm, same harness, same
# output.
import sys

sys.setrecursionlimit(10000)


def mines_around(board, r, c):
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            y, x = r + dr, c + dc
            if (dr != 0 or dc != 0) and 0 <= y < len(board) and 0 <= x < len(board[0]):
                if board[y][x] in ("M", "X"):
                    count += 1
    return count


def reveal(board, r, c):
    if board[r][c] != "E":
        return
    count = mines_around(board, r, c)
    if count > 0:
        board[r][c] = chr(48 + count)
        return
    board[r][c] = "B"
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            y, x = r + dr, c + dc
            if 0 <= y < len(board) and 0 <= x < len(board[0]):
                reveal(board, y, x)


def update_board(board, click):
    r, c = click
    if board[r][c] == "M":
        board[r][c] = "X"
    else:
        reveal(board, r, c)
    return board


def parse(rows):
    return [list(row) for row in rows]


def show(board):
    return "/".join("".join(row) for row in board)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_board(m, n, percent):
    return [["M" if next_random() % 100 < percent else "E" for _ in range(n)] for _ in range(m)]


def random_unrevealed(board):
    open_ = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] in ("E", "M")]
    if not open_:
        return (-1, -1)
    return open_[next_random() % len(open_)]


def main():
    global seed
    after = update_board(parse(["EEEEE", "EEMEE", "EEEEE", "EEEEE"]), [3, 0])
    print(f"example 1: {show(after)}")
    print(f"example 2: {show(update_board(after, [1, 2]))}")
    print(f"one square: {show(update_board(parse(['E']), [0, 0]))} and {show(update_board(parse(['M']), [0, 0]))}")
    print(f"a digit: {show(update_board(parse(['EM', 'EE']), [1, 0]))}")
    print(f"walled off: {show(update_board(parse(['EEMEE', 'EEMEE', 'MMMEE']), [0, 0]))}")
    seed = 529
    checksum = 0
    blanks = 0
    exploded = 0
    for _ in range(500):
        m = 1 + next_random() % 12
        n = 1 + next_random() % 12
        board = random_board(m, n, next_random() % 31)
        for _ in range(3):
            r, c = random_unrevealed(board)
            if r < 0:
                break
            board = update_board(board, [r, c])
        for row in board:
            for ch in row:
                if ch == "B":
                    blanks += 1
                if ch == "X":
                    exploded += 1
                checksum = (checksum * 31 + ord(ch)) % 1000000007
    print(f"500 random boards: {blanks} blank, {exploded} exploded, checksum {checksum}")
    board = random_board(50, 50, 2)
    c = 0
    while board[0][c] == "M":
        c += 1
    board = update_board(board, [0, c])
    counts = [0, 0, 0]
    for row in board:
        for ch in row:
            if ch == "B":
                counts[0] += 1
            elif ch in ("E", "M"):
                counts[1] += 1
            else:
                counts[2] += 1
    print(f"50 by 50, clicked at (0, {c}): {counts[0]} blank, {counts[1]} unrevealed, {counts[2]} digits; row 0 {show([board[0]])}")


main()
