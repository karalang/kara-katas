# Benchmark for #490: Python mirror of the ★ arm (breadth first over
# stopping cells); see the_maze.kara.
from collections import deque


def has_path(maze, start, destination):
    rows = len(maze)
    cols = len(maze[0])
    seen = [[False] * cols for _ in range(rows)]
    queue = deque([(start[0], start[1])])
    seen[start[0]][start[1]] = True
    while queue:
        row, col = queue.popleft()
        if row == destination[0] and col == destination[1]:
            return True
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r, c = row, col
            while 0 <= r + dr < rows and 0 <= c + dc < cols and maze[r + dr][c + dc] == 0:
                r += dr
                c += dc
            if not seen[r][c]:
                seen[r][c] = True
                queue.append((r, c))
    return False


def main():
    # 60 mazes of 300 by 300 cells, a wall in each cell with odds of 1 in
    # 6, and a start and a destination on open cells, built once, then
    # each solved once.
    n = 300
    seed = 490

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    mazes, starts, destinations = [], [], []
    for _ in range(60):
        maze = [[1 if next_random() % 6 == 0 else 0 for _ in range(n)] for _ in range(n)]
        start = [next_random() % n, next_random() % n]
        destination = [next_random() % n, next_random() % n]
        maze[start[0]][start[1]] = 0
        maze[destination[0]][destination[1]] = 0
        mazes.append(maze)
        starts.append(start)
        destinations.append(destination)
    reached = 0
    checksum = 0
    for k in range(len(mazes)):
        found = has_path(mazes[k], starts[k], destinations[k])
        if found:
            reached += 1
        checksum = (checksum * 31 + (7 if found else 3)) % 1000000007
    print(f"60 mazes of 300 by 300: the destination reached in {reached}, checksum {checksum}")


main()
