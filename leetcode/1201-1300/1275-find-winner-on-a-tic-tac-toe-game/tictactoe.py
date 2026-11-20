# LeetCode #1275: Find Winner on a Tic Tac Toe Game -- Python mirror of the
# ★ arm: line sums, A adding 1 and B taking 1 away.


def tictactoe(moves):
    rows = [0, 0, 0]
    cols = [0, 0, 0]
    diagonal = 0
    anti = 0
    turn = 1
    for r, c in moves:
        rows[r] += turn
        cols[c] += turn
        if r == c:
            diagonal += turn
        if r + c == 2:
            anti += turn
        if abs(rows[r]) == 3 or abs(cols[c]) == 3 or abs(diagonal) == 3 or abs(anti) == 3:
            return "A" if turn == 1 else "B"
        turn = -turn
    return "Draw" if len(moves) == 9 else "Pending"


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


KIND = {"A": 0, "B": 1, "Draw": 2, "Pending": 3}


def walk(moves, tally, check):
    for square in range(9):
        r, c = square // 3, square % 3
        if any(m[0] == r and m[1] == c for m in moves):
            continue
        moves.append([r, c])
        k = KIND[tictactoe(moves)]
        tally[k] += 1
        check = (check * 7 + k) % 1000000007
        if k == 3:
            check = walk(moves, tally, check)
        moves.pop()
    return check


def main():
    global seed
    a = tictactoe([[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]])
    b = tictactoe([[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]])
    d = tictactoe([[0, 0], [1, 1], [2, 0], [1, 0], [1, 2], [2, 1], [0, 1], [0, 2], [2, 2]])
    print(f"{a} {b} {d}")
    tally = [0, 0, 0, 0]
    check = walk([], tally, 0)
    print(f"{sum(tally)} positions: A {tally[0]}, B {tally[1]}, Draw {tally[2]}, Pending {tally[3]}, checksum {check}")
    seed = 1275
    check = 0
    tally = [0, 0, 0, 0]
    for _ in range(3000):
        order = list(range(9))
        for i in range(8, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        moves = []
        stop = 1 + next_random() % 9
        for square in order:
            moves.append([square // 3, square % 3])
            if len(moves) == stop or tictactoe(moves) != "Pending":
                break
        k = KIND[tictactoe(moves)]
        tally[k] += 1
        check = (check * 131 + k * 10 + len(moves)) % 1000000007
    print(f"3000 random games: A {tally[0]}, B {tally[1]}, Draw {tally[2]}, Pending {tally[3]}, checksum {check}")


main()
