# LeetCode #1730: Shortest Path to Get Food -- the bench (food.kara): a
# breadth-first search from you, the first food off the queue the
# nearest.
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
    r = next_random(seed) % 20000
    return "X" if r < 5000 else ("#" if r < 5001 else "O")


def main():
    count = 10
    rounds = 200
    side = 200
    seed = [1730]
    problems = []
    for _ in range(count):
        grid = [[cell(seed) for _ in range(side)] for _ in range(side)]
        at = (next_random(seed) * 32768 + next_random(seed)) % (side * side)
        grid[at // side][at % side] = "*"
        problems.append(grid)
    total = 0
    check = 0
    for r in range(rounds):
        for grid in problems:
            answer = get_food(grid)
            total += answer
            check = (check * 31 + answer + 1 + r) % 1000000007
    print(f"{count} grids of {side} by {side}, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
