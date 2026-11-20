# LeetCode #1275 bench, in Python: the ★ arm (line sums) asked about every
# position of every game of tic-tac-toe, 549,945 of them, each game carried
# on while the answer is "Pending"; 40 rounds, every answer folded into a
# checksum.
import sys

sys.setrecursionlimit(100)


def tictactoe(moves):
    rows = [0, 0, 0]
    cols = [0, 0, 0]
    diagonal = 0
    anti = 0
    turn = 1
    for m in moves:
        r, c = m[0], m[1]
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


def walk(moves, check):
    for square in range(9):
        r, c = square // 3, square % 3
        if any(m[0] == r and m[1] == c for m in moves):
            continue
        moves.append([r, c])
        answer = tictactoe(moves)
        k = 0 if answer == "A" else 1 if answer == "B" else 2 if answer == "Draw" else 3
        check = (check * 7 + k) % 1000000007
        if k == 3:
            check = walk(moves, check)
        moves.pop()
    return check


def main():
    check = 0
    for rnd in range(40):
        check = walk([], check)
        check = (check * 131 + rnd) % 1000000007
    print(f"40 rounds of every game: checksum {check}")


main()
