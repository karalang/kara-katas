# LeetCode #688: Knight Probability in Chessboard -- the chances, forward.
# Bench.
#
# 60 queries, boards of 15 to 25 squares a side and 50 to 100 moves from
# a random start, are drawn once; then 50 rounds answer every query.

DR = [2, 1, -1, -2, -2, -1, 1, 2]
DC = [1, 2, 2, 1, -1, -2, -2, -1]


def knight_probability(n, k, row, column):
    board = [0.0] * (n * n)
    board[row * n + column] = 1.0
    for _ in range(k):
        nxt = [0.0] * (n * n)
        for r in range(n):
            for c in range(n):
                p = board[r * n + c]
                if p > 0.0:
                    for m in range(8):
                        r2 = r + DR[m]
                        c2 = c + DC[m]
                        if 0 <= r2 < n and 0 <= c2 < n:
                            nxt[r2 * n + c2] += p / 8.0
        board = nxt
    total = 0.0
    for p in board:
        total += p
    return total


seed = 688


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 60
    rounds = 50
    queries = []
    for _ in range(count):
        n = 15 + next_random() % 11
        k = 50 + next_random() % 51
        row = next_random() % n
        column = next_random() % n
        queries.append((n, k, row, column))
    total = 0.0
    for _ in range(rounds):
        for n, k, row, column in queries:
            total += knight_probability(n, k, row, column)
    print(f"{count * rounds} queries answered, sum {total:.6f}")


main()
