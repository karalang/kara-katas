# LeetCode #576: Out of Boundary Paths -- the ways forward, move by move.
#
# Python mirror of find_paths.kara (the starred arm): each move sends
# every cell's paths to its four neighbours, those outside the grid
# counted in the answer, modulo 10^9 + 7.


def find_paths(m, n, max_move, start_row, start_column):
    modulus = 1000000007
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ways = [[0] * n for _ in range(m)]
    ways[start_row][start_column] = 1
    out = 0
    for _ in range(max_move):
        nxt = [[0] * n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                here = ways[r][c]
                if here == 0:
                    continue
                for dr, dc in moves:
                    nr = r + dr
                    nc = c + dc
                    if nr < 0 or nr >= m or nc < 0 or nc >= n:
                        out = (out + here) % modulus
                    else:
                        nxt[nr][nc] = (nxt[nr][nc] + here) % modulus
        ways = nxt
    return out


# ---- test harness -----------------------------------------------------------

seed = 576


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(m, n, max_move, start_row, start_column):
    print(f"{m} by {n}, {max_move} moves from ({start_row}, {start_column}): "
          f"{find_paths(m, n, max_move, start_row, start_column)}")


def main():
    show(2, 2, 2, 0, 0)
    show(1, 3, 3, 0, 1)
    show(3, 3, 0, 1, 1)
    show(1, 1, 1, 0, 0)
    show(1, 1, 50, 0, 0)
    show(1, 5, 2, 0, 2)
    show(5, 1, 2, 2, 0)
    show(5, 5, 2, 2, 2)
    show(5, 5, 3, 2, 2)
    total = 0
    checksum = 0
    for _ in range(300):
        m = 1 + step() % 10
        n = 1 + step() % 10
        max_move = step() % 13
        r = step() % m
        c = step() % n
        got = find_paths(m, n, max_move, r, c)
        total = (total + got) % 1000000007
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")
    show(50, 50, 50, 0, 0)
    show(50, 50, 50, 25, 25)
    show(50, 50, 50, 0, 24)


main()
