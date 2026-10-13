# LeetCode #490: The Maze -- breadth first over the places the ball stops.
# Mirrors the_maze.kara (the ★ arm).
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
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row, col
            while 0 <= r + dr < rows and 0 <= c + dc < cols and maze[r + dr][c + dc] == 0:
                r += dr
                c += dc
            if not seen[r][c]:
                seen[r][c] = True
                queue.append((r, c))
    return False


def show(name, maze, start, destination):
    found = "true" if has_path(maze, start, destination) else "false"
    print(f"{name}: from [{start[0]}, {start[1]}] to [{destination[0]}, {destination[1]}] -> {found}")


seed = 490


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    first = [
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    show("example 1", first, [0, 4], [4, 4])
    show("example 2", first, [0, 4], [3, 2])
    show("example 3", [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 0, 0],
    ], [4, 3], [0, 1])
    show("two cells", [[0, 0]], [0, 0], [0, 1])
    show("the middle of a row", [[0, 0, 0]], [0, 0], [0, 1])
    show("a column", [[0], [0], [0], [0]], [3, 0], [0, 0])
    show("an open room's corner", [[0] * 4 for _ in range(3)], [1, 1], [2, 3])
    show("an open room's middle", [[0] * 4 for _ in range(3)], [0, 0], [1, 2])
    count = 300
    reached = 0
    checksum = 0
    made = 0
    while made < count:
        odds = 20 if made % 3 == 0 else 33 if made % 3 == 1 else 50
        rows = 1 + next_random() % 12
        cols = 1 + next_random() % 12
        maze = [[1 if next_random() % 100 < odds else 0 for _ in range(cols)] for _ in range(rows)]
        start = [next_random() % rows, next_random() % cols]
        destination = [next_random() % rows, next_random() % cols]
        if start == destination:
            continue
        maze[start[0]][start[1]] = 0
        maze[destination[0]][destination[1]] = 0
        made += 1
        found = has_path(maze, start, destination)
        if found:
            reached += 1
        checksum = (checksum * 31 + (7 if found else 3) + rows * cols) % 1000000007
    print(f"{count} random mazes: the destination reached in {reached}, checksum {checksum}")


main()
