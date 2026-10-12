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


def show(text):
    board = [list(row) for row in text.split("/")]
    print(f"{text}: {count_battleships(board)}")


show("X..X/...X/...X")
show(".")
show("X")
show("XXXX")
show("X/X/X")
show("X.X.X/...../X.X.X")
show("XX.XX/...../XXXXX")
show("X..../X.XXX/X..../....X/X...X")
show("...../...../.....")
total = 0
checksum = 0
for _ in range(1000):
    rows = 1 + step() % 12
    cols = 1 + step() % 12
    board = [["."] * cols for _ in range(rows)]
    tries = step() % 20
    for _ in range(tries):
        length = 1 + step() % 4
        across = step() % 2 == 0
        r = step() % rows
        c = step() % cols
        dr, dc = (0, 1) if across else (1, 0)
        fits = r + dr * (length - 1) < rows and c + dc * (length - 1) < cols
        if fits:
            for k in range(-1, length + 1):
                for side in range(-1, 2):
                    rr = r + dr * k + dc * side
                    cc = c + dc * k + dr * side
                    if 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == "X":
                        fits = False
        if fits:
            for k in range(length):
                board[r + dr * k][c + dc * k] = "X"
    answer = count_battleships(board)
    total += answer
    checksum = (checksum * 31 + answer + rows * cols) % 1000000007
print(f"1000 random boards: {total} ships, checksum {checksum}")
