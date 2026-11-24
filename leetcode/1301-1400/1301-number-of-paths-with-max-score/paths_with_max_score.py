# LeetCode #1301: Number of Paths with Max Score -- Python mirror of the ★
# arm (a table from the bottom-right corner back, each square holding the
# most points reaching it and how many paths collect that many).


def paths_with_max_score(board):
    n = len(board)
    modulus = 1000000007
    best = [[-1] * n for _ in range(n)]
    ways = [[0] * n for _ in range(n)]
    best[n - 1][n - 1] = 0
    ways[n - 1][n - 1] = 1
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if board[i][j] == 'X' or (i == n - 1 and j == n - 1):
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
                c = board[i][j]
                points = int(c) if c.isdigit() else 0
                best[i][j] = top + points
                ways[i][j] = count
    if best[0][0] < 0:
        return [0, 0]
    return [best[0][0], ways[0][0]]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return f"{v[0]},{v[1]}"


def make_board(n, wall):
    board = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == 0 and j == 0:
                row.append('E')
            elif i == n - 1 and j == n - 1:
                row.append('S')
            elif next_random() % 100 < wall:
                row.append('X')
            else:
                row.append(str(next_random() % 9 + 1))
        board.append(''.join(row))
    return board


def main():
    global seed
    e1 = paths_with_max_score(["E23", "2X2", "12S"])
    e2 = paths_with_max_score(["E12", "1X1", "21S"])
    e3 = paths_with_max_score(["E11", "XXX", "11S"])
    e4 = paths_with_max_score(["EX", "XS"])
    e5 = paths_with_max_score(["E5", "5S"])
    print(f"{show(e1)} {show(e2)} {show(e3)} {show(e4)} {show(e5)}")
    seed = 1301
    total = 0
    none = 0
    check = 0
    for i in range(602):
        n = 2 + next_random() % 29 if i < 600 else 100
        wall = next_random() % 61 if i < 600 else (0 if i == 600 else 20)
        got = paths_with_max_score(make_board(n, wall))
        if got[1] == 0:
            none += 1
        total += got[0]
        check = (check * 131 + got[0]) % 1000000007
        check = (check * 131 + got[1]) % 1000000007
    print(f"602 random boards: {none} with no path, scores total {total}, checksum {check}")


main()
