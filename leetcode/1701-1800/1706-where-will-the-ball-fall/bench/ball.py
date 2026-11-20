# LeetCode #1706: Where Will the Ball Fall -- the bench's Python mirror:
# the ★ arm on 1000 random boxes of 100 by 100, all drawn first, each
# answered 100 times.


def find_ball(grid):
    # each ball followed down a row at a time
    n = len(grid[0])
    answer = []
    for start in range(n):
        c = start
        for row in grid:
            nxt = c + row[c]
            if nxt < 0 or nxt >= n or row[nxt] != row[c]:
                c = -1
                break
            c = nxt
        answer.append(c)
    return answer


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count, rounds, side = 1000, 100, 100
    seed = [1706]
    boxes = []
    for _ in range(count):
        # long runs of one slope: a board turns the other way one time in 20
        grid = []
        for _ in range(side):
            row = []
            board = 1
            for _ in range(side):
                if next_random(seed) % 20 == 0:
                    board = -board
                row.append(board)
            grid.append(row)
        boxes.append(grid)
    out = 0
    check = 0
    for r in range(rounds):
        for grid in boxes:
            for a in find_ball(grid):
                if a >= 0:
                    out += 1
                check = (check * 31 + a + 2 + r) % 1000000007
    print(f"{count} boxes of {side} by {side}, {rounds} rounds: {out} balls out, checksum {check}")


main()
