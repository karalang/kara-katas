"""LeetCode #37 bench — Python (mirror of sudoku_solver.kara).

Bitmask backtracking solver over a flat list[int] board with three nine-element mask
lists, linear cell order, ascending digit order, XOR undo. Workload: TOTAL times copy
the "world's hardest sudoku" template, clear cell k%81, solve in place, fold a
position-weighted signature of the solved grid into a checksum. Same sink as the Kāra /
C / Rust / Go mirrors — the slow interpreted lane in the runtime table.
"""

TOTAL = 500
MODULUS = 1000000007

TEMPLATE = [
    8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 9, 0, 2, 0, 0,
    0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 4, 5, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0,
    0, 0, 1, 0, 0, 0, 0, 6, 8, 0, 0, 8, 5, 0, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 4, 0, 0,
]


def box_index(r: int, c: int) -> int:
    return (r // 3) * 3 + c // 3


def go(board, rows, cols, boxes, pos: int) -> bool:
    if pos == 81:
        return True
    r, c = divmod(pos, 9)
    if board[pos] != 0:
        return go(board, rows, cols, boxes, pos + 1)
    b = box_index(r, c)
    used = rows[r] | cols[c] | boxes[b]
    d = 1
    while d <= 9:
        bit = 1 << d
        if (used & bit) == 0:
            board[pos] = d
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if go(board, rows, cols, boxes, pos + 1):
                return True
            board[pos] = 0
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
        d += 1
    return False


def solve(board) -> bool:
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for i in range(81):
        d = board[i]
        if d != 0:
            r, c = divmod(i, 9)
            bit = 1 << d
            rows[r] |= bit
            cols[c] |= bit
            boxes[box_index(r, c)] |= bit
    return go(board, rows, cols, boxes, 0)


def main() -> None:
    acc = 0
    for k in range(TOTAL):
        work = TEMPLATE[:]
        work[k % 81] = 0
        solve(work)
        sig = 0
        for i in range(81):
            sig += work[i] * (i + 1)
        acc = (acc * 31 + sig) % MODULUS
    print(acc)


if __name__ == "__main__":
    main()
