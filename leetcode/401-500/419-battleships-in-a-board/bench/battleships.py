# LeetCode #419: Battleships in a Board -- mirror of battleships.kara
# (count the first cells).


def count_battleships(board):
    count = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == "X" and (r == 0 or board[r - 1][c] != "X") and (c == 0 or board[r][c - 1] != "X"):
                count += 1
    return count


seed = 419


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def clear(board, r, c):
    n = len(board)
    for rr, cc in ((r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
        if 0 <= rr < n and 0 <= cc < n and board[rr][cc] == "X":
            return False
    return True


def main():
    n = 200
    rounds = 20000
    board = [["."] * n for _ in range(n)]
    for _ in range(4000):
        length = 1 + step() % 4
        across = step() % 2 == 0
        r = step() % n
        c = step() % n
        dr, dc = (0, 1) if across else (1, 0)
        fits = r + dr * (length - 1) < n and c + dc * (length - 1) < n
        for k in range(length):
            if fits and not clear(board, r + dr * k, c + dc * k):
                fits = False
        if fits:
            for k in range(length):
                board[r + dr * k][c + dc * k] = "X"
    total = 0
    checksum = 0
    for _ in range(rounds):
        r = step() % n
        c = step() % n
        if board[r][c] == "X":
            board[r][c] = "."
            if not clear(board, r, c):
                board[r][c] = "X"
        elif clear(board, r, c):
            board[r][c] = "X"
        answer = count_battleships(board)
        total += answer
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{rounds} rounds on a {n}x{n} board: total {total}, checksum {checksum}")


main()
