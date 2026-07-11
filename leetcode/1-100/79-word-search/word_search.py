"""LeetCode #79: Word Search — DFS backtracking with in-place cell marking.

Mirror of word_search.kara. Depth-first search from every cell matching word[0];
the current cell is temporarily blanked (a sentinel that no board letter equals)
so the path can't reuse it, the four neighbours are explored, and the cell is
restored on the way out. Same nine cases and output shape (a `word: true/false`
line per case, then a `sink:` fold of the boolean outcomes) so the files diff
line-for-line.
"""

from __future__ import annotations


def dfs(board: list[list[int]], word: list[int], r: int, c: int, k: int,
        rows: int, cols: int) -> bool:
    if k == len(word):
        return True
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False
    if board[r][c] != word[k]:
        return False
    saved = board[r][c]
    board[r][c] = 0
    found = (dfs(board, word, r + 1, c, k + 1, rows, cols)
             or dfs(board, word, r - 1, c, k + 1, rows, cols)
             or dfs(board, word, r, c + 1, k + 1, rows, cols)
             or dfs(board, word, r, c - 1, k + 1, rows, cols))
    board[r][c] = saved
    return found


def exists(board: list[list[int]], word: list[int]) -> bool:
    rows = len(board)
    if rows == 0:
        return len(word) == 0
    cols = len(board[0])
    if len(word) == 0:
        return True
    for r in range(rows):
        for c in range(cols):
            if dfs(board, word, r, c, 0, rows, cols):
                return True
    return False


def make_board(rows: list[str]) -> list[list[int]]:
    return [[b for b in row.encode()] for row in rows]


def report(rows: list[str], word: str, acc: list[int]) -> None:
    board = make_board(rows)
    wvec = list(word.encode())
    found = exists(board, wvec)
    print(f"{word}: {'true' if found else 'false'}")
    bit = 1 if found else 0
    acc[0] = (acc[0] * 131 + bit + 1) % 1000000007


def main() -> None:
    board_rows = ["ABCE", "SFCS", "ADEE"]
    acc = [0]
    report(board_rows, "ABCCED", acc)
    report(board_rows, "SEE", acc)
    report(board_rows, "ABCB", acc)
    report(board_rows, "SFDA", acc)
    report(board_rows, "ABCESEEEFS", acc)
    report(board_rows, "A", acc)
    report(board_rows, "Z", acc)
    report(["A"], "A", acc)
    report(["A"], "AB", acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
