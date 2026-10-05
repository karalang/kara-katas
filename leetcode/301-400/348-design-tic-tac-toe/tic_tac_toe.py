# LeetCode #348 -- Design Tic-Tac-Toe. Python mirror of tic_tac_toe.kara (the
# star arm): one counter per row, column and diagonal; player 1 adds 1,
# player 2 subtracts 1, and a line is won when its counter reaches +-n.


class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = 0
        self.anti = 0

    def make_move(self, row, col, player):
        d = 1 if player == 1 else -1
        self.rows[row] += d
        self.cols[col] += d
        if row == col:
            self.diag += d
        if row + col == self.n - 1:
            self.anti += d
        goal = d * self.n
        if goal in (self.rows[row], self.cols[col], self.diag, self.anti):
            return player
        return 0


def play(n, moves):
    game = TicTacToe(n)
    out = []
    player = 1
    for r, c in moves:
        w = game.make_move(r, c, player)
        out.append(w)
        if w != 0:
            break
        player = 3 - player
    return out


def shuffled_cells(n, seed):
    cells = [(r, c) for r in range(n) for c in range(n)]
    x = seed
    k = len(cells) - 1
    while k > 0:
        x = (x * 1103515245 + 12345) % 2147483648
        j = x // 16 % (k + 1)
        cells[k], cells[j] = cells[j], cells[k]
        k -= 1
    return cells


def show(label, results):
    print(f"{label}: [{', '.join(str(v) for v in results)}]")


def main():
    show("example", play(3, [(0, 0), (0, 2), (2, 2), (1, 1), (2, 0), (1, 0), (2, 1)]))
    show("one cell", play(1, [(0, 0)]))
    show("column", play(3, [(0, 0), (0, 1), (2, 2), (1, 1), (1, 0), (2, 1)]))
    show("anti-diagonal", play(4, [(0, 3), (0, 0), (1, 2), (0, 1), (2, 1), (1, 1), (3, 0)]))
    show("draw", play(3, [(0, 0), (1, 1), (2, 2), (0, 1), (2, 1), (2, 0), (0, 2), (1, 2), (1, 0)]))
    games = wins1 = wins2 = total_moves = 0
    for n in range(1, 41):
        for g in range(25):
            result = play(n, shuffled_cells(n, n * 1000 + g))
            games += 1
            total_moves += len(result)
            if result[-1] == 1:
                wins1 += 1
            elif result[-1] == 2:
                wins2 += 1
    print(f"{games} random games: player 1 won {wins1}, player 2 won {wins2}, {total_moves} moves")


main()
