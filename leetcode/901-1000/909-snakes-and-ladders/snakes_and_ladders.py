# LeetCode #909: Snakes and Ladders -- a breadth-first search over the
# squares. Mirrors snakes_and_ladders.kara.


def cell(board, square):
    n = len(board)
    row = (square - 1) // n
    col = (square - 1) % n if row % 2 == 0 else n - 1 - (square - 1) % n
    return board[n - 1 - row][col]


def snakes_and_ladders(board):
    n = len(board)
    last = n * n
    moves = [-1] * (last + 1)
    queue = [1]
    moves[1] = 0
    head = 0
    while head < len(queue):
        s = queue[head]
        head += 1
        if s == last:
            return moves[s]
        for roll in range(1, 7):
            if s + roll > last:
                break
            here = cell(board, s + roll)
            nxt = s + roll if here == -1 else here
            if moves[nxt] == -1:
                moves[nxt] = moves[s] + 1
                queue.append(nxt)
    return -1


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def place(n, goes):
    board = [[-1] * n for _ in range(n)]
    for s in range(1, n * n + 1):
        row = (s - 1) // n
        col = (s - 1) % n if row % 2 == 0 else n - 1 - (s - 1) % n
        board[n - 1 - row][col] = goes[s]
    return board


def random_board(n, rare, down):
    last = n * n
    goes = [-1] * (last + 1)
    for s in range(2, last):
        if next_random() % rare == 0:
            goes[s] = 1 + next_random() % (s - 1) if down else 1 + next_random() % last
    return place(n, goes)


def show(board):
    listed = ",".join("[" + ",".join(str(x) for x in row) + "]" for row in board)
    print(f"board = [{listed}] -> {snakes_and_ladders(board)}")


def main():
    global seed
    show([
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 35, -1, -1, 13, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 15, -1, -1, -1, -1],
    ])
    show([[-1, -1], [-1, 3]])
    show([[-1, -1], [-1, -1]])
    show([[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]])
    show([[1, -1, -1], [1, 1, 1], [-1, 1, 1]])
    show([[-1, -1, -1, -1], [-1, 16, -1, -1], [-1, -1, -1, -1], [-1, 10, -1, -1]])
    show([[-1, -1, -1], [-1, -1, -1], [-1, 9, -1]])
    seed = 909
    total = 0
    stuck = 0
    check = 0
    for c in range(300):
        n = 2 + next_random() % 19
        rare = 1 if c % 4 == 0 else 4 if c % 4 == 1 else 30 if c % 4 == 2 else 2
        got = snakes_and_ladders(random_board(n, rare, c % 4 == 3))
        if got == -1:
            stuck += 1
        else:
            total += got
        check = (check * 1000003 + got + 2) % 1000000007
    print(f"300 boards: {stuck} unreachable, the rest summing to {total}, checksum {check}")
    print(f"20 x 20 empty -> {snakes_and_ladders(place(20, [-1] * 401))}")
    print(f"20 x 20 random, 1 in 4 -> {snakes_and_ladders(random_board(20, 4, False))}")
    print(f"20 x 20 random, 1 in 20 -> {snakes_and_ladders(random_board(20, 20, False))}")


main()
