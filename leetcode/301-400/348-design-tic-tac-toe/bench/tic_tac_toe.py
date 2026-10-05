# Benchmark workload for LeetCode #348 — Python mirror of tic_tac_toe.kara.

SIDE = 1000
GAMES = 100


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
        if self.rows[row] == goal or self.cols[col] == goal or self.diag == goal or self.anti == goal:
            return player
        return 0


def main():
    cells = SIDE * SIDE
    order = list(range(cells))
    x = 348
    k = cells - 1
    while k > 0:
        x = (x * 1103515245 + 12345) % 2147483648
        j = x // 16 % (k + 1)
        order[k], order[j] = order[j], order[k]
        k -= 1

    sink = 0
    for g in range(GAMES):
        start = g * cells // GAMES
        game = TicTacToe(SIDE)
        player, moves, winner = 1, 0, 0
        while moves < cells and winner == 0:
            cell = order[(start + moves) % cells]
            winner = game.make_move(cell // SIDE, cell % SIDE, player)
            moves += 1
            player = 3 - player
        sink = (sink * 31 + moves * (winner + 1)) % 1000000007
    print(f"sink {sink}")


main()
