# Benchmark for #529: Python mirror of the ★ arm (reveal recursively);
# see update_board.kara. The same seeded generator, so the same boards
# and clicks; a fresh copy of the board per click.
import sys

sys.setrecursionlimit(10000)


def mines_around(board, r, c):
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            y, x = r + dr, c + dc
            if (dr != 0 or dc != 0) and 0 <= y < len(board) and 0 <= x < len(board[0]):
                if board[y][x] == "M" or board[y][x] == "X":
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


seed = 529


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    boards = []
    for _ in range(50):
        percent = next_random() % 21
        boards.append([["M" if next_random() % 100 < percent else "E" for _ in range(50)] for _ in range(50)])
    opened = exploded = checksum = 0
    for _ in range(400):
        for b in range(len(boards)):
            r = next_random() % 50
            c = next_random() % 50
            after = update_board([row[:] for row in boards[b]], [r, c])
            shown = 0
            for row in after:
                for ch in row:
                    if ch == "X":
                        exploded += 1
                    elif ch != "E" and ch != "M":
                        shown += 1
            opened += shown
            checksum = (checksum * 31 + shown) % 1000000007
    print(f"50 boards of 50 by 50, 400 rounds of clicks: {opened} opened, {exploded} exploded, checksum {checksum}")


main()
