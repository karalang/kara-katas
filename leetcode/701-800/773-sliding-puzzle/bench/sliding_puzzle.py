# LeetCode 773 — Sliding Puzzle: benchmark, the ★ arm in Python.
# All 720 boards, in dictionary order, built once; ROUNDS rounds each
# solve the next of them.
from collections import deque

ROUNDS = 20000
NEIGHBOURS = [[1, 3], [0, 2, 4], [1, 5], [0, 4], [1, 3, 5], [2, 4]]


def sliding_puzzle(board):
    start = "".join(str(x) for row in board for x in row)
    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        state, steps = queue.popleft()
        if state == "123450":
            return steps
        zero = state.index("0")
        for nxt in NEIGHBOURS[zero]:
            moved = list(state)
            moved[zero], moved[nxt] = moved[nxt], moved[zero]
            text = "".join(moved)
            if text not in seen:
                seen.add(text)
                queue.append((text, steps + 1))
    return -1


def next_order(cells):
    i = len(cells) - 2
    while i >= 0 and cells[i] >= cells[i + 1]:
        i -= 1
    if i < 0:
        return False
    j = len(cells) - 1
    while cells[j] <= cells[i]:
        j -= 1
    cells[i], cells[j] = cells[j], cells[i]
    cells[i + 1:] = reversed(cells[i + 1:])
    return True


def main():
    boards = []
    cells = [0, 1, 2, 3, 4, 5]
    while True:
        boards.append([cells[0:3], cells[3:6]])
        if not next_order(cells):
            break
    solved = check = 0
    for r in range(ROUNDS):
        answer = sliding_puzzle(boards[r % 720])
        if answer >= 0:
            solved += 1
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{ROUNDS} boards: {solved} solvable, checksum {check}")


main()
