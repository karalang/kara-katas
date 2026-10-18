# LeetCode #723: Candy Crush -- crushed cells marked by their sign.
# Benchmark mirror of the Kara star arm: each round marks every run of
# three across or down by negating its cells, then drops each column,
# until a round marks nothing; the board is crushed on a copy.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def candy_crush(board):
    b = [row[:] for row in board]
    m, n = len(b), len(b[0])
    stable = False
    while not stable:
        stable = True
        for r in range(m):
            for c in range(n - 2):
                v = abs(b[r][c])
                if v != 0 and abs(b[r][c + 1]) == v and abs(b[r][c + 2]) == v:
                    b[r][c] = b[r][c + 1] = b[r][c + 2] = -v
                    stable = False
        for r in range(m - 2):
            for c in range(n):
                v = abs(b[r][c])
                if v != 0 and abs(b[r + 1][c]) == v and abs(b[r + 2][c]) == v:
                    b[r][c] = b[r + 1][c] = b[r + 2][c] = -v
                    stable = False
        for c in range(n):
            write = m - 1
            for r in range(m - 1, -1, -1):
                if b[r][c] > 0:
                    b[write][c] = b[r][c]
                    write -= 1
            while write >= 0:
                b[write][c] = 0
                write -= 1
    return b


def main():
    seed = [723]
    boards = [[[1 + next_random(seed) % 5 for _ in range(50)] for _ in range(50)] for _ in range(40)]
    total = 0
    for rnd in range(100):
        for d in range(40):
            r, c = (rnd * 7 + d) % 50, (rnd * 13 + d * 3) % 50
            boards[d][r][c] = 1 + (boards[d][r][c] + rnd) % 5
            after = candy_crush(boards[d])
            total += sum(row.count(0) for row in after)
    print(f"100 rounds of 40 boards of 50 x 50: {total} empty cells")


main()
