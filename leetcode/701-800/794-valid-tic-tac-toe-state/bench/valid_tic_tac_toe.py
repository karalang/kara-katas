# LeetCode 794 -- Valid Tic-Tac-Toe State: the bench, in Python. Mirrors
# valid_tic_tac_toe.kara: count the marks and check the lines.

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
    boards = [random_board() for _ in range(4096)]
    rounds = 6000000
    valid = 0
    check = 0
    for r in range(rounds):
        if valid_tic_tac_toe(boards[r % 4096]):
            valid += 1
            check = (check * 131 + r % 4096) % 1000000007
    print(f"{rounds} boards: {valid} valid, checksum {check}")


main()
