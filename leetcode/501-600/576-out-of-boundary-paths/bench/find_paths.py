# Benchmark for #576: Python mirror of the ★ arm (the ways forward, move
# by move); see find_paths.kara.


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


# ---- benchmark ----------------------------------------------------------------

seed = 576


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 5000
    total = 0
    checksum = 0
    for _ in range(count):
        m = 30 + next_random() % 21
        n = 30 + next_random() % 21
        max_move = 30 + next_random() % 21
        r = next_random() % m
        c = next_random() % n
        got = find_paths(m, n, max_move, r, c)
        total = (total + got) % 1000000007
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} cases up to 50 by 50 and 50 moves: total {total}, checksum {checksum}")


main()
