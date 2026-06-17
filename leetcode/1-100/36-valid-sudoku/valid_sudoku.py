"""LeetCode #36: Valid Sudoku — known-correct reference oracle.

Algorithmic mirror of valid_sudoku.kara (the single-pass bitmask style ★). Output
format matches line-for-line so the two can be diffed directly. The boolean-matrix
and three-pass variants produce identical verdicts; this oracle additionally
cross-checks all three algorithms agree on every board (and against a brute-force
check that enumerates each row/column/box and looks for a repeated digit).

Boards use 0 for an empty cell and 1..9 for a placed digit (the Kāra encoding); the
'.'-character board of the LeetCode statement maps onto 0 directly.
"""

from __future__ import annotations


def box_index(r: int, c: int) -> int:
    return (r // 3) * 3 + c // 3


# --- Style 1: single-pass digit bitmasks (mirrors valid_sudoku.kara) -----------

def is_valid_bitmask(board: list[list[int]]) -> bool:
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d != 0:
                bit = 1 << d
                b = box_index(r, c)
                if (rows[r] & bit) or (cols[c] & bit) or (boxes[b] & bit):
                    return False
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
    return True


# --- Style 2: boolean seen-matrices (mirrors valid_sudoku_bool.kara) -----------

def is_valid_bool(board: list[list[int]]) -> bool:
    seen_row = [[False] * 10 for _ in range(9)]
    seen_col = [[False] * 10 for _ in range(9)]
    seen_box = [[False] * 10 for _ in range(9)]
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d != 0:
                b = box_index(r, c)
                if seen_row[r][d] or seen_col[c][d] or seen_box[b][d]:
                    return False
                seen_row[r][d] = True
                seen_col[c][d] = True
                seen_box[b][d] = True
    return True


# --- Style 3: three independent passes (mirrors valid_sudoku_passes.kara) -------

def is_valid_passes(board: list[list[int]]) -> bool:
    for r in range(9):
        mask = 0
        for c in range(9):
            d = board[r][c]
            if d != 0:
                bit = 1 << d
                if mask & bit:
                    return False
                mask |= bit
    for c in range(9):
        mask = 0
        for r in range(9):
            d = board[r][c]
            if d != 0:
                bit = 1 << d
                if mask & bit:
                    return False
                mask |= bit
    for b in range(9):
        mask = 0
        br, bc = (b // 3) * 3, (b % 3) * 3
        for i in range(3):
            for j in range(3):
                d = board[br + i][bc + j]
                if d != 0:
                    bit = 1 << d
                    if mask & bit:
                        return False
                    mask |= bit
    return True


# --- Brute-force ground truth (enumerate each unit, look for a repeat) ---------

def _unit_ok(values: list[int]) -> bool:
    seen = set()
    for d in values:
        if d != 0:
            if d in seen:
                return False
            seen.add(d)
    return True


def is_valid_brute(board: list[list[int]]) -> bool:
    for r in range(9):
        if not _unit_ok([board[r][c] for c in range(9)]):
            return False
    for c in range(9):
        if not _unit_ok([board[r][c] for r in range(9)]):
            return False
    for b in range(9):
        br, bc = (b // 3) * 3, (b % 3) * 3
        if not _unit_ok([board[br + i][bc + j] for i in range(3) for j in range(3)]):
            return False
    return True


def board_empty() -> list[list[int]]:
    return [[0] * 9 for _ in range(9)]


def board_example1() -> list[list[int]]:
    return [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]


def board_example2() -> list[list[int]]:
    b = board_example1()
    b[0][0] = 8  # top-left 5 -> 8: repeats in column 0 (row 3) and the top-left box
    return b


def board_solved() -> list[list[int]]:
    return [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]


def board_row_dup() -> list[list[int]]:
    b = board_empty()
    b[0][0] = 1
    b[0][8] = 1
    return b


def board_col_dup() -> list[list[int]]:
    b = board_empty()
    b[0][0] = 2
    b[8][0] = 2
    return b


def board_box_dup() -> list[list[int]]:
    b = board_empty()
    b[0][0] = 3
    b[1][1] = 3
    return b


CASES = [
    ("example1 (valid partial)", board_example1()),
    ("example2 (col+box dup)  ", board_example2()),
    ("empty board            ", board_empty()),
    ("solved board           ", board_solved()),
    ("row-only duplicate     ", board_row_dup()),
    ("col-only duplicate     ", board_col_dup()),
    ("box-only duplicate     ", board_box_dup()),
]


def main() -> None:
    for name, board in CASES:
        a = is_valid_bitmask(board)
        b = is_valid_bool(board)
        c = is_valid_passes(board)
        truth = is_valid_brute(board)
        assert a == b == c == truth, (name, a, b, c, truth)
        print(f"{name} -> {'valid' if a else 'invalid'}")


if __name__ == "__main__":
    main()
