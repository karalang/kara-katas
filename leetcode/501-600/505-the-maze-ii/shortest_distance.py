# LeetCode #505: The Maze II -- Python mirror of the ★ arm (Dijkstra over
# the cells the ball can stop in); see shortest_distance.kara. heapq is
# smallest-first, as PriorityQueue.new() is.
import heapq


def shortest_distance(maze, start, destination):
    rows = len(maze)
    cols = len(maze[0])
    best = [[-1] * cols for _ in range(rows)]
    queue = [(0, start[0], start[1])]
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        d, r, c = heapq.heappop(queue)
        if best[r][c] != -1:
            continue
        best[r][c] = d
        if r == destination[0] and c == destination[1]:
            return d
        for dr, dc in moves:
            nr, nc, steps = r, c, 0
            while 0 <= nr + dr < rows and 0 <= nc + dc < cols and maze[nr + dr][nc + dc] == 0:
                nr += dr
                nc += dc
                steps += 1
            if steps > 0 and best[nr][nc] == -1:
                heapq.heappush(queue, (d + steps, nr, nc))
    return -1


# ---- test harness ---------------------------------------------------------


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(name, maze, start, destination):
    print(f"{name}: from {fmt(start)} to {fmt(destination)} -> {shortest_distance(maze, start, destination)}")


seed = 505


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
    show("rolls past", [[0, 0, 0, 0, 0]], [0, 4], [0, 2])
    show("a column", [[0], [0], [0], [0]], [3, 0], [0, 0])
    # The far corner of an open room, two rolls either way.
    show("a room", [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [0, 0], [2, 2])
    show("walled in", [[0, 1, 0], [1, 1, 0], [0, 0, 0]], [0, 0], [2, 2])
    # The short way is a dead end: the ball stops only by the long one.
    show("the long way", [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0]], [0, 0], [2, 0])
    # 300 random mazes of 1 to 12 by 1 to 12 cells, a wall in each cell
    # with odds of 1 in 5, 1 in 3 or 1 in 2 in turn, with a start and a
    # destination in two different open cells.
    count = 300
    reached = 0
    total = 0
    checksum = 0
    for k in range(count):
        rows = 1 + next_random() % 12
        cols = 1 + next_random() % 12
        odds = 5 if k % 3 == 0 else 3 if k % 3 == 1 else 2
        maze = []
        open_cells = []
        for r in range(rows):
            line = []
            for c in range(cols):
                if next_random() % odds == 0:
                    line.append(1)
                else:
                    line.append(0)
                    open_cells.append((r, c))
            maze.append(line)
        if len(open_cells) < 2:
            continue
        a = next_random() % len(open_cells)
        b = next_random() % (len(open_cells) - 1)
        if b >= a:
            b += 1
        sr, sc = open_cells[a]
        dr, dc = open_cells[b]
        d = shortest_distance(maze, [sr, sc], [dr, dc])
        if d != -1:
            reached += 1
            total += d
        checksum = (checksum * 31 + d + 1) % 1000000007
    print(f"{count} random mazes: the destination reached in {reached}, distance {total} in all, checksum {checksum}")


main()
