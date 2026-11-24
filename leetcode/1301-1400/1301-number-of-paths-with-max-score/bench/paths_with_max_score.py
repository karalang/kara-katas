# LeetCode #1301 bench: the ★ arm (a table from the bottom-right corner
# back, each square holding the most points reaching it and how many paths
# collect that many) over 20 boards of 100 by 100 with obstacles 0 to 38 in
# 100, built once; then 150 passes, each setting one square of every board to
# an obstacle or a digit from the checksum so far, answering it, and folding
# the score and the count into the checksum.


def paths_with_max_score(board):
    grid = [list(row) for row in board]
    n = len(grid)
    modulus = 1000000007
    best = [[-1] * n for _ in range(n)]
    ways = [[0] * n for _ in range(n)]
    best[n - 1][n - 1] = 0
    ways[n - 1][n - 1] = 1
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if grid[i][j] == 'X' or (i == n - 1 and j == n - 1):
                continue
            top = -1
            count = 0
            for a, b in ((i + 1, j), (i, j + 1), (i + 1, j + 1)):
                if a < n and b < n and best[a][b] >= 0:
                    if best[a][b] > top:
                        top = best[a][b]
                        count = ways[a][b]
                    elif best[a][b] == top:
                        count = (count + ways[a][b]) % modulus
            if top >= 0:
                c = grid[i][j]
                points = ord(c) - 48 if '0' <= c <= '9' else 0
                best[i][j] = top + points
                ways[i][j] = count
    if best[0][0] < 0:
        return [0, 0]
    return [best[0][0], ways[0][0]]


seed = 1301


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    boards = []
    for t in range(20):
        wall = 2 * t
        board = []
        for i in range(100):
            row = []
            for j in range(100):
                if i == 0 and j == 0:
                    row.append('E')
                elif i == 99 and j == 99:
                    row.append('S')
                elif next_random() % 100 < wall:
                    row.append('X')
                else:
                    row.append(str(next_random() % 9 + 1))
            board.append(''.join(row))
        boards.append(board)
    check = 0
    for p in range(150):
        for board in boards:
            at = 1 + check % 9998
            i, j = at // 100, at % 100
            cells = list(board[i])
            cells[j] = 'X' if check % 7 == 0 else str(check % 9 + 1)
            board[i] = ''.join(cells)
            got = paths_with_max_score(board)
            check = (check * 31 + got[0] + p) % 1000000007
            check = (check * 31 + got[1]) % 1000000007
    print(f"150 passes over 20 boards of 100 by 100: checksum {check}")


main()
