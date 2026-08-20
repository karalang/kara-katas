"""Oracle mirror for LeetCode 289 — same algorithm as game_of_life.kara.

The two-bit in-place encoding, spelled in Python: bit 0 is the old generation
and is never written during the sweep, bit 1 is the new one. `& 1` on every
neighbour read is what keeps the sweep order irrelevant.
"""


def live_neighbours(board, r, c):
    rows, cols = len(board), len(board[0])
    n = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if 0 <= rr < rows and 0 <= cc < cols:
                n += board[rr][cc] & 1
    return n


def step(board):
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            n = live_neighbours(board, r, c)
            alive = (board[r][c] & 1) == 1
            lives = (n in (2, 3)) if alive else (n == 3)
            if lives:
                board[r][c] |= 2
    for r in range(rows):
        for c in range(cols):
            board[r][c] >>= 1


def render(board):
    return "".join(
        "".join("#" if v == 1 else "." for v in row) + "\n" for row in board
    )


def report(label, board, steps):
    print(f"{label}:")
    for _ in range(steps):
        step(board)
    print(render(board), end="")
    print("")


def main():
    report("example after 1 step", [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]], 1)

    blinker = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    report("blinker after 1 step", blinker, 1)
    report("blinker after 2 steps (back to start)", blinker, 1)

    report("block after 3 steps (still life)", [[1, 1], [1, 1]], 3)

    glider = [
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    report("glider after 4 steps (shifted 1,1)", glider, 4)

    report("lone cell dies", [[0, 0, 0], [0, 1, 0], [0, 0, 0]], 1)


if __name__ == "__main__":
    main()
