# LeetCode #909: Snakes and Ladders -- bench program, Python.
#
# A breadth-first search over the squares, on one 20 x 20 board, LeetCode's
# largest, built once. Each round changes one square, to a snake or ladder
# to a random square or to none, solves the board and folds the answer
# into a checksum.


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


seed = 909


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 20
    last = n * n
    rounds = 100000
    board = [[-1] * n for _ in range(n)]
    stuck = 0
    total = 0
    check = 0
    for _ in range(rounds):
        s = 2 + next_random() % (last - 2)
        row = (s - 1) // n
        col = (s - 1) % n if row % 2 == 0 else n - 1 - (s - 1) % n
        board[n - 1 - row][col] = -1 if next_random() % 2 == 0 else 1 + next_random() % last
        got = snakes_and_ladders(board)
        if got == -1:
            stuck += 1
        else:
            total += got
        check = (check * 31 + got + 2) % 1000000007
    print(f"{rounds} rounds on a 20 x 20 board: {stuck} with the end out of reach, the rest summing to {total}, checksum {check}")


main()
