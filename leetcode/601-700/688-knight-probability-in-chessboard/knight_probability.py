# LeetCode #688: Knight Probability in Chessboard -- the chances, forward.
#
# A mirror of knight_probability.kara (the ★ arm) and its harness.

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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(n, k, row, column):
    print(f"n = {n}, k = {k}, start ({row}, {column}): {knight_probability(n, k, row, column):.5f}")


def main():
    show(3, 2, 0, 0)
    show(1, 0, 0, 0)
    show(1, 1, 0, 0)
    show(2, 3, 1, 0)
    show(3, 1, 1, 1)
    show(8, 0, 7, 7)
    show(8, 1, 3, 4)
    show(8, 30, 0, 0)
    show(25, 100, 12, 12)
    show(25, 100, 0, 0)
    show(25, 100, 24, 13)

    line = ""
    for k in [1, 10, 50, 100]:
        scale = 1.0
        for _ in range(k):
            scale *= 4.0
        if k != 1:
            line += ","
        line += f" k = {k}: {knight_probability(3, k, 0, 2) * scale:.5f}"
    print(f"3 x 3 from a corner, times 4^k:{line}")

    queries = zeros = ones = 0
    total = 0.0
    for n in range(1, 9):
        for k in range(7):
            for r in range(n):
                for c in range(n):
                    p = knight_probability(n, k, r, c)
                    queries += 1
                    if p == 0.0:
                        zeros += 1
                    if p == 1.0:
                        ones += 1
                    total += p
    print(f"{queries} small queries: {zeros} certain to fall off, {ones} certain to stay, sum {total:.5f}")

    low, high, total = 1.0, 0.0, 0.0
    for r in range(12):
        for c in range(12):
            p = knight_probability(12, 20, r, c)
            low = min(low, p)
            high = max(high, p)
            total += p
    print(f"12 x 12, 20 moves, every start: lowest {low:.5f}, highest {high:.5f}, sum {total:.5f}")

    seed = [688]
    checksum = 0.0
    for _ in range(200):
        n = 1 + next_random(seed) % 25
        k = next_random(seed) % 51
        r = next_random(seed) % n
        c = next_random(seed) % n
        checksum += knight_probability(n, k, r, c)
    print(f"200 random queries: sum {checksum:.5f}")


main()
