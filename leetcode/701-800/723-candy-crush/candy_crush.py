# LeetCode #723: Candy Crush -- crushed cells marked by their sign.
#
# A mirror of candy_crush.kara (the ★ arm) and its harness.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_board(m, n, kinds, seed):
    return [[1 + next_random(seed) % kinds for _ in range(n)] for _ in range(m)]


def fold(board, start):
    total = start
    for row in board:
        for v in row:
            total = (total * 31 + v) % 1000000007
    return total


def empty(board):
    return sum(row.count(0) for row in board)


def show(board):
    print(candy_crush(board))


def main():
    show([
        [110, 5, 112, 113, 114], [210, 211, 5, 213, 214], [310, 311, 3, 313, 314],
        [410, 411, 412, 5, 414], [5, 1, 512, 3, 3], [610, 4, 1, 613, 614],
        [710, 1, 2, 713, 714], [810, 1, 2, 1, 1], [1, 1, 2, 2, 2], [4, 1, 4, 4, 1014],
    ])
    show([[1, 3, 5, 5, 2], [3, 4, 3, 3, 1], [3, 2, 4, 5, 2], [2, 4, 4, 5, 5], [1, 4, 4, 1, 1]])
    show([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    show([[7, 7, 7], [7, 7, 7], [7, 7, 7]])
    show([[1, 1, 1], [2, 2, 1], [3, 4, 1]])
    show([[2, 2, 2, 2, 2], [1, 3, 3, 3, 3], [4, 5, 6, 7, 8]])
    show([[1, 5, 6], [2, 7, 8], [2, 9, 4], [2, 1, 1]])
    show([[1, 2, 3], [1, 2, 3], [1, 4, 3], [5, 4, 6], [5, 4, 6], [5, 7, 6]])
    seed = [723]
    for kinds in range(3, 6):
        after = candy_crush(random_board(50, 50, kinds, seed))
        print(f"50 x 50 board of {kinds} kinds: {empty(after)} empty, checksum {fold(after, 0)}")
    total = 0
    for _ in range(300):
        m = 3 + next_random(seed) % 6
        n = 3 + next_random(seed) % 6
        kinds = 1 + next_random(seed) % 4
        total = fold(candy_crush(random_board(m, n, kinds, seed)), total)
    print(f"300 random boards: checksum {total}")


main()
