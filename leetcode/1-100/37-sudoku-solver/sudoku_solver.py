"""LeetCode #37: Sudoku Solver — known-correct reference oracle.

Algorithmic mirror of sudoku_solver.kara (the bitmask-backtracking style ★). Output
format matches line-for-line so the two can be diffed directly. The plain re-scan and
MRV variants find the SAME solution on a unique-solution board; this oracle additionally
cross-checks all three algorithms agree on every puzzle (and against a brute-force
solution counter that proves each test puzzle has exactly one completion — the property
that makes "the solution" well defined and the three orders interchangeable).

Boards use 0 for an empty cell and 1..9 for a placed digit (the Kāra encoding); the
'.'-character board of the LeetCode statement maps onto 0 directly. #37 is the dual of
#36: where #36 *validates* a board, #37 *completes* one — the example puzzle here solves
to exactly the board #36's example validated.
"""

from __future__ import annotations

from copy import deepcopy


def box_index(r: int, c: int) -> int:
    return (r // 3) * 3 + c // 3


# --- Style 1: bitmask backtracking (mirrors sudoku_solver.kara, ★) -------------
#
# Carry three nine-element bitmask arrays (rows / cols / boxes): bit d set means
# "digit d already placed in this unit". A cell's legal digits are exactly those whose
# bit is clear in rows[r] | cols[c] | boxes[b]. Scan cells linearly; at the first empty
# one, try each legal digit ascending, set its three bits, recurse, and on failure clear
# them (undo) and try the next. The masks make the candidate test O(1) and the undo a
# single XOR per unit — no per-placement re-scan of the grid.

def solve_bitmask(board: list[list[int]]) -> bool:
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d != 0:
                bit = 1 << d
                rows[r] |= bit
                cols[c] |= bit
                boxes[box_index(r, c)] |= bit

    def go(pos: int) -> bool:
        if pos == 81:
            return True
        r, c = divmod(pos, 9)
        if board[r][c] != 0:
            return go(pos + 1)
        b = box_index(r, c)
        used = rows[r] | cols[c] | boxes[b]
        d = 1
        while d <= 9:
            bit = 1 << d
            if (used & bit) == 0:
                board[r][c] = d
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
                if go(pos + 1):
                    return True
                board[r][c] = 0
                rows[r] &= ~bit
                cols[c] &= ~bit
                boxes[b] &= ~bit
            d += 1
        return False

    return go(0)


# --- Style 2: plain backtracking, re-scan validity (mirrors *_plain.kara) -------
#
# No carried state: at each empty cell, test a candidate by scanning its row, column,
# and box for that digit right then. More work per placement (O(27) per test vs O(1)),
# but the purest reading of backtracking — "place a digit that doesn't conflict, recurse,
# undo if stuck" — with the conflict test spelled out where it happens.

def is_safe(board: list[list[int]], r: int, c: int, d: int) -> bool:
    for i in range(9):
        if board[r][i] == d or board[i][c] == d:
            return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[br + i][bc + j] == d:
                return False
    return True


def solve_plain(board: list[list[int]]) -> bool:
    def go(pos: int) -> bool:
        if pos == 81:
            return True
        r, c = divmod(pos, 9)
        if board[r][c] != 0:
            return go(pos + 1)
        d = 1
        while d <= 9:
            if is_safe(board, r, c, d):
                board[r][c] = d
                if go(pos + 1):
                    return True
                board[r][c] = 0
            d += 1
        return False

    return go(0)


# --- Style 3: MRV — fewest-candidates-first (mirrors sudoku_solver_mrv.kara) -----
#
# Same bitmask candidate test, but instead of the next linear empty cell, branch on the
# empty cell with the FEWEST legal digits (minimum remaining values). A cell with one
# candidate is forced — taking it first collapses the search tree dramatically on hard
# puzzles. On a unique-solution board the completion is the same; only the node count
# (and so the path to it) differs.

def solve_mrv(board: list[list[int]]) -> bool:
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d != 0:
                bit = 1 << d
                rows[r] |= bit
                cols[c] |= bit
                boxes[box_index(r, c)] |= bit

    def candidates(r: int, c: int) -> int:
        return (~(rows[r] | cols[c] | boxes[box_index(r, c)])) & 0x3FE  # bits 1..9

    def popcount(x: int) -> int:
        n = 0
        while x:
            x &= x - 1
            n += 1
        return n

    def go(remaining: int) -> bool:
        if remaining == 0:
            return True
        # Pick the empty cell with the fewest candidates.
        best_r = best_c = -1
        best_n = 10
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    n = popcount(candidates(r, c))
                    if n < best_n:
                        best_n, best_r, best_c = n, r, c
                        if n <= 1:
                            break
            if best_n <= 1:
                break
        r, c = best_r, best_c
        b = box_index(r, c)
        cand = candidates(r, c)
        d = 1
        while d <= 9:
            bit = 1 << d
            if (cand & bit) != 0:
                board[r][c] = d
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
                if go(remaining - 1):
                    return True
                board[r][c] = 0
                rows[r] &= ~bit
                cols[c] &= ~bit
                boxes[b] &= ~bit
            d += 1
        return False

    empties = sum(1 for r in range(9) for c in range(9) if board[r][c] == 0)
    return go(empties)


# --- Brute-force solution counter (ground truth + uniqueness proof) -------------

def count_solutions(board: list[list[int]], cap: int = 2) -> int:
    """Count completions up to `cap` (cap=2 distinguishes none / unique / multiple)."""
    work = deepcopy(board)
    total = 0

    def go(pos: int) -> None:
        nonlocal total
        if total >= cap:
            return
        if pos == 81:
            total += 1
            return
        r, c = divmod(pos, 9)
        if work[r][c] != 0:
            go(pos + 1)
            return
        for d in range(1, 10):
            if is_safe(work, r, c, d):
                work[r][c] = d
                go(pos + 1)
                work[r][c] = 0
                if total >= cap:
                    return

    go(0)
    return total


# --- Test puzzles (0 = empty). Each verified below for solution count. -----------

def board_example() -> list[list[int]]:
    # LeetCode #37 example 1 — the exact board #36's example 1 validates.
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


def board_escargot() -> list[list[int]]:
    # "AI Escargot" (Arto Inkala, 2006) — a classic backtracking-heavy unique puzzle.
    return [
        [1, 0, 0, 0, 0, 7, 0, 9, 0],
        [0, 3, 0, 0, 2, 0, 0, 0, 8],
        [0, 0, 9, 6, 0, 0, 5, 0, 0],
        [0, 0, 5, 3, 0, 0, 9, 0, 0],
        [0, 1, 0, 0, 8, 0, 0, 0, 2],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 0, 0],
    ]


def board_inkala() -> list[list[int]]:
    # Arto Inkala's 2012 "world's hardest sudoku" — unique, maximal backtracking.
    return [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]


def board_solved() -> list[list[int]]:
    # Already complete (0 empties) — every solver returns it unchanged.
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


def board_unsolvable() -> list[list[int]]:
    # Valid SO FAR but with no completion: cell (0,0)'s row already holds {1..6} and its
    # box already holds {7,8,9}, so no digit 1..9 fits there — the search must fail.
    b = [[0] * 9 for _ in range(9)]
    b[0][3], b[0][4], b[0][5], b[0][6], b[0][7], b[0][8] = 1, 2, 3, 4, 5, 6
    b[1][1], b[1][2], b[2][1] = 7, 8, 9
    return b


CASES = [
    ("example  (LeetCode 37)", board_example(), 1),
    ("escargot (AI Escargot) ", board_escargot(), 1),
    ("inkala   (hardest 2012)", board_inkala(), 1),
    ("solved   (0 empties)   ", board_solved(), 1),
    ("unsolvable (no fill)   ", board_unsolvable(), 0),
]


def fmt(board: list[list[int]]) -> str:
    return "/".join("".join(str(d) for d in row) for row in board)


def main() -> None:
    for name, board, expected_count in CASES:
        # Ground truth: prove the completion count is what we expect (internal — the
        # uniqueness is what makes the three styles' found solution identical; it is not
        # printed, so the line-for-line diff against the Kāra mirror stays clean).
        got = count_solutions(board)
        assert got == expected_count, (name, got, expected_count)

        # All three styles must agree with each other (and, when solvable, find the
        # unique completion — identical because the solution is unique).
        outs = []
        for solve in (solve_bitmask, solve_plain, solve_mrv):
            work = deepcopy(board)
            ok = solve(work)
            outs.append((ok, fmt(work) if ok else "no solution"))
        a, b, c = outs
        assert a == b == c, (name, a, b, c)

        ok, rendered = a
        assert ok == (expected_count > 0), (name, ok, expected_count)
        print(f"{name} -> {rendered}")


if __name__ == "__main__":
    main()
