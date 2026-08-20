"""Benchmark twin for LeetCode #289 — same algorithm as gameoflife.kara."""

ROWS = COLS = 256
GENS = 60


def next_rand(s):
    return (s * 1103515245 + 12345) & 2147483647


def main():
    seed = 20260820
    board = [[0] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            seed = next_rand(seed)
            board[r][c] = 1 if ((seed // 65536) % 100) < 35 else 0

    for _ in range(GENS):
        for r in range(ROWS):
            for c in range(COLS):
                n = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < ROWS and 0 <= cc < COLS:
                            n += board[rr][cc] & 1
                alive = (board[r][c] & 1) == 1
                lives = (n in (2, 3)) if alive else (n == 3)
                if lives:
                    board[r][c] |= 2
        for r in range(ROWS):
            for c in range(COLS):
                board[r][c] >>= 1

    pop = hash_ = 0
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 1:
                pop += 1
                hash_ = (hash_ * 31 + (r * COLS + c)) % 1000000007
    print(f"pop {pop} hash {hash_}")


if __name__ == "__main__":
    main()
