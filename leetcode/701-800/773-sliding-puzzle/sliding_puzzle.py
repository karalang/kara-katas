# LeetCode 773 — Sliding Puzzle: the ★ arm and harness in Python.
from collections import deque

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


def show(board):
    print(f"{board} -> {sliding_puzzle(board)}")


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
    show([[1, 2, 3], [4, 0, 5]])
    show([[1, 2, 3], [5, 4, 0]])
    show([[4, 1, 2], [5, 0, 3]])
    show([[1, 2, 3], [4, 5, 0]])
    show([[3, 2, 4], [1, 5, 0]])
    show([[0, 1, 2], [3, 4, 5]])
    cells = [0, 1, 2, 3, 4, 5]
    boards = solvable = total = most = check = 0
    while True:
        answer = sliding_puzzle([cells[0:3], cells[3:6]])
        boards += 1
        if answer >= 0:
            solvable += 1
            total += answer
            most = max(most, answer)
        check = (check * 31 + answer + 1) % 1000000007
        if not next_order(cells):
            break
    print(f"all {boards} boards: {solvable} solvable, {total} moves in all, at most {most}, checksum {check}")


main()
