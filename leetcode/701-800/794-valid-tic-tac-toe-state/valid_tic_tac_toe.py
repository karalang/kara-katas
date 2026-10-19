# LeetCode 794 -- Valid Tic-Tac-Toe State, by the rules. Python mirror of
# the ★ arm and its harness.

LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


def wins(cells, mark):
    return any(cells[a] == mark and cells[b] == mark and cells[c] == mark for a, b, c in LINES)


def valid_tic_tac_toe(board):
    cells = "".join(board)
    x = cells.count("X")
    o = cells.count("O")
    if x != o and x != o + 1:
        return False
    if wins(cells, "X") and x != o + 1:
        return False
    if wins(cells, "O") and x != o:
        return False
    return True


seed = 794


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(rows):
    answer = "true" if valid_tic_tac_toe(rows) else "false"
    print(f'["{rows[0]}", "{rows[1]}", "{rows[2]}"] -> {answer}')


def random_board():
    cells = [" "] * 9
    if next_random() % 2 == 0:
        marks = [" ", "X", "O"]
        for i in range(9):
            cells[i] = marks[next_random() % 3]
    else:
        moves = next_random() % 10
        mover = "X"
        for _ in range(moves):
            empty = [i for i in range(9) if cells[i] == " "]
            cells[empty[next_random() % len(empty)]] = mover
            mover = "O" if mover == "X" else "X"
    return ["".join(cells[r * 3 : r * 3 + 3]) for r in range(3)]


def main():
    show(["O  ", "   ", "   "])
    show(["XOX", " X ", "   "])
    show(["XOX", "O O", "XOX"])
    show(["   ", "   ", "   "])
    show(["XXX", "OO ", "   "])
    show(["XXX", "XOO", "OO "])
    show(["XXX", "   ", "OOO"])
    show(["XO ", "XO ", "XO "])
    show(["XOX", "XOO", "XXO"])
    valid = 0
    check = 0
    for i in range(300):
        board = random_board()
        if valid_tic_tac_toe(board):
            valid += 1
            check = (check * 131 + i) % 1000000007
    print(f"300 random boards: {valid} valid, checksum {check}")


main()
