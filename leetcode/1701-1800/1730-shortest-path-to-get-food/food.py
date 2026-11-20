# LeetCode #1730: Shortest Path to Get Food -- the Python mirror of the ★
# arm, food.kara: a breadth-first search from you, the first food off the
# queue the nearest.
from collections import deque


def get_food(grid):
    rows = len(grid)
    cols = len(grid[0])
    distance = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "*":
                distance[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        if grid[r][c] == "#":
            return distance[r][c]
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] != "X" and distance[nr][nc] < 0:
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr, nc))
    return -1


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def cell(seed):
    r = next_random(seed) % 20
    return "X" if r < 5 else ("#" if r < 7 else "O")


def batch(count, most, seed):
    found = 0
    total = 0
    check = 0
    for _ in range(count):
        rows = next_random(seed) % most + 1
        cols = next_random(seed) % most + 1
        grid = [[cell(seed) for _ in range(cols)] for _ in range(rows)]
        at = next_random(seed) % (rows * cols)
        grid[at // cols][at % cols] = "*"
        answer = get_food(grid)
        if answer >= 0:
            found += 1
            total += answer
        check = (check * 31 + answer + 1 + rows * cols) % 1000000007
    print(f"{count} grids of up to {most} by {most}: food reached {found} times, steps sum to {total}, checksum {check}")


def main():
    for lines in [
        ["XXXXXX", "X*OOOX", "XOO#OX", "XXXXXX"],
        ["XXXXX", "X*XOX", "XOX#X", "XXXXX"],
        ["XXXXXXXX", "X*OXO#OX", "XOOXOOXX", "XOOOO#OX", "XXXXXXXX"],
        ["*"],
        ["*OOOO", "XXXXO", "#OOOO"],
    ]:
        print(get_food([list(line) for line in lines]))
    seed = [1730]
    batch(3000, 5, seed)
    batch(300, 50, seed)
    batch(5, 200, seed)


main()
