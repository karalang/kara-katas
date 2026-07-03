"""LeetCode #51: N-Queens — algorithmic mirror of marker_arrays.kara (the ★ solver).

Row-by-row backtracking with three boolean marker arrays (columns, ↘ diagonals
keyed by row+col, ↙ diagonals keyed by row-col+(n-1)). Scans columns 0..n-1 in
increasing order at every level, so the solution listing comes out in exactly the
same canonical order the three .kara solvers produce — this oracle diffs
byte-for-byte against `karac run` / `karac build` output for all of them.
"""

from __future__ import annotations


def build_board(queens: list[int], n: int) -> list[str]:
    board = []
    for r in range(n):
        qc = queens[r]
        board.append("".join("Q" if c == qc else "." for c in range(n)))
    return board


def solve(n: int) -> list[list[str]]:
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)          # ↘, keyed by row + col
    diag2 = [False] * (2 * n - 1)          # ↙, keyed by row - col + (n - 1)
    queens: list[int] = []
    out: list[list[str]] = []

    def place(row: int) -> None:
        if row == n:
            out.append(build_board(queens, n))
            return
        for c in range(n):
            d1 = row + c
            d2 = row - c + (n - 1)
            if not cols[c] and not diag1[d1] and not diag2[d2]:
                cols[c] = diag1[d1] = diag2[d2] = True
                queens.append(c)
                place(row + 1)
                queens.pop()
                cols[c] = diag1[d1] = diag2[d2] = False

    place(0)
    return out


def report(n: int) -> None:
    sols = solve(n)
    print(f"n={n} -> {len(sols)}")
    for board in sols:
        for row in board:
            print(row)
        print("--")
    print("====")


def main() -> None:
    report(1)
    report(2)
    report(3)
    report(4)
    report(5)
    report(6)

    counts = " ".join(str(len(solve(n))) for n in range(1, 10))
    print(f"counts: {counts}")


if __name__ == "__main__":
    main()
