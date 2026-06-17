#!/usr/bin/env python3
"""LeetCode #36 bench — Python (mirror of valid_sudoku.kara).

Single-pass bitmask validation of a 9x9 board with three nine-element mask lists,
perturb-validate-restore TOTAL times with the verdict folded into a checksum. Same
sink as every other mirror.
"""


def box_index(r, c):
    return (r // 3) * 3 + c // 3


def is_valid(board):
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            d = board[r * 9 + c]
            if d != 0:
                bit = 1 << d
                b = box_index(r, c)
                if (rows[r] & bit) or (cols[c] & bit) or (boxes[b] & bit):
                    return False
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
    return True


def main():
    total = 5000000
    modulus = 1000000007

    board = [
        5, 3, 4, 6, 7, 8, 9, 1, 2, 6, 7, 2, 1, 9, 5, 3, 4, 8, 1, 9, 8, 3, 4, 2, 5, 6, 7, 8, 5, 9,
        7, 6, 1, 4, 2, 3, 4, 2, 6, 8, 5, 3, 7, 9, 1, 7, 1, 3, 9, 2, 4, 8, 5, 6, 9, 6, 1, 5, 3, 7,
        2, 8, 4, 2, 8, 7, 4, 1, 9, 6, 3, 5, 3, 4, 5, 2, 8, 6, 1, 7, 9,
    ]

    acc = 0
    for k in range(total):
        pos = k % 81
        digit = (k % 9) + 1
        save = board[pos]
        board[pos] = digit
        v = 1 if is_valid(board) else 0
        acc = (acc * 31 + v) % modulus
        board[pos] = save

    print(acc)


if __name__ == "__main__":
    main()
