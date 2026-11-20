# LeetCode #1728: Cat and Mouse II -- the bench (mouse.kara): the game
# solved backwards from its ends, a state lost for the player to move once
# every move from it is counted off.
from collections import deque


def reach(marks, at, jump):
    rows = len(marks)
    cols = len(marks[0])
    r, c = at // cols, at % cols
    cells = [at]
    for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        for k in range(1, jump + 1):
            nr, nc = r + dr * k, c + dc * k
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols or marks[nr][nc] == "#":
                break
            cells.append(nr * cols + nc)
    return cells


def can_mouse_win(grid, cat_jump, mouse_jump):
    marks = [list(row) for row in grid]
    cols = len(marks[0])
    cells = len(marks) * cols
    mouse = cat = food = 0
    for at in range(cells):
        ch = marks[at // cols][at % cols]
        if ch == "M":
            mouse = at
        elif ch == "C":
            cat = at
        elif ch == "F":
            food = at
    open_ = [marks[at // cols][at % cols] != "#" for at in range(cells)]
    mouse_moves = [reach(marks, at, mouse_jump) if open_[at] else [] for at in range(cells)]
    cat_moves = [reach(marks, at, cat_jump) if open_[at] else [] for at in range(cells)]

    def state(m, c, turn):
        return (m * cells + c) * 2 + turn

    result = [0] * (cells * cells * 2)
    left = [0] * (cells * cells * 2)
    queue = deque()
    for m in range(cells):
        for c in range(cells):
            if not open_[m] or not open_[c]:
                continue
            left[state(m, c, 0)] = len(mouse_moves[m])
            left[state(m, c, 1)] = len(cat_moves[c])
            end = 2 if (m == c or c == food) else (1 if m == food else 0)
            if end != 0:
                for turn in range(2):
                    result[state(m, c, turn)] = end
                    queue.append(state(m, c, turn))
    while queue:
        s = queue.popleft()
        turn = s % 2
        m = s // 2 // cells
        c = s // 2 % cells
        won = result[s]
        if turn == 0:
            for before in cat_moves[c]:
                p = state(m, before, 1)
                if result[p] != 0:
                    continue
                if won == 2:
                    result[p] = 2
                    queue.append(p)
                else:
                    left[p] -= 1
                    if left[p] == 0:
                        result[p] = 1
                        queue.append(p)
        else:
            for before in mouse_moves[m]:
                p = state(before, c, 0)
                if result[p] != 0:
                    continue
                if won == 1:
                    result[p] = 1
                    queue.append(p)
                else:
                    left[p] -= 1
                    if left[p] == 0:
                        result[p] = 2
                        queue.append(p)
    return result[state(mouse, cat, 0)] == 1


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 200
    rounds = 20
    side = 8
    cells = side * side
    seed = [1728]
    problems = []
    for _ in range(count):
        marks = ["#" if next_random(seed) % 4 == 0 else "." for _ in range(cells)]
        places = list(range(cells))
        for i in range(3):
            j = i + next_random(seed) % (cells - i)
            places[i], places[j] = places[j], places[i]
        marks[places[0]] = "C"
        marks[places[1]] = "M"
        marks[places[2]] = "F"
        grid = ["".join(marks[r * side:(r + 1) * side]) for r in range(side)]
        cat_jump = next_random(seed) % side + 1
        mouse_jump = next_random(seed) % side + 1
        problems.append((grid, cat_jump, mouse_jump))
    wins = 0
    check = 0
    for r in range(rounds):
        for grid, cat_jump, mouse_jump in problems:
            answer = can_mouse_win(grid, cat_jump, mouse_jump)
            if answer:
                wins += 1
            check = (check * 31 + (2 if answer else 1) + r) % 1000000007
    print(f"{count} grids of {side} by {side}, {rounds} rounds: the mouse wins {wins}, checksum {check}")


main()
