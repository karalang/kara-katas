# LeetCode #499: The Maze III -- Dijkstra over the places the ball stops.
# Mirrors the_maze_iii.kara (the ★ arm); output is byte-identical.
import heapq


def find_shortest_way(maze, ball, hole):
    rows = len(maze)
    cols = len(maze[0])
    moves = [(1, 0, "d"), (0, -1, "l"), (0, 1, "r"), (-1, 0, "u")]
    done = [[False] * cols for _ in range(rows)]
    queue = [(0, "", ball[0], ball[1])]
    while queue:
        dist, path, row, col = heapq.heappop(queue)
        if done[row][col]:
            continue
        done[row][col] = True
        if row == hole[0] and col == hole[1]:
            return path
        for dr, dc, name in moves:
            r = row
            c = col
            steps = 0
            while 0 <= r + dr < rows and 0 <= c + dc < cols and maze[r + dr][c + dc] == 0:
                r += dr
                c += dc
                steps += 1
                if r == hole[0] and c == hole[1]:
                    break
            if steps > 0 and not done[r][c]:
                heapq.heappush(queue, (dist + steps, path + name, r, c))
    return "impossible"


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(name, maze, ball, hole):
    print(f"{name}: from {fmt(ball)} to {fmt(hole)} -> {find_shortest_way(maze, ball, hole)}")


seed = 499


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    first = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 0, 0],
    ]
    show("example 1", first, [4, 3], [0, 1])
    show("example 2", first, [4, 3], [3, 0])
    show("example 3", [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
    ], [0, 4], [3, 5])
    show("two cells", [[0, 0]], [0, 0], [0, 1])
    show("a hole mid-row", [[0, 0, 0, 0, 0]], [0, 4], [0, 2])
    show("a column", [[0], [0], [0], [0]], [3, 0], [0, 0])
    show("a tie", [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [0, 0], [2, 2])
    show("walled in", [[0, 1, 0], [1, 1, 0], [0, 0, 0]], [0, 0], [2, 2])
    count = 300
    reached = 0
    letters = 0
    checksum = 0
    for k in range(count):
        rows = 1 + next_random() % 12
        cols = 1 + next_random() % 12
        odds = 5 if k % 3 == 0 else (3 if k % 3 == 1 else 2)
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
        br, bc = open_cells[a]
        hr, hc = open_cells[b]
        way = find_shortest_way(maze, [br, bc], [hr, hc])
        if way != "impossible":
            reached += 1
            letters += len(way)
        for ch in way:
            checksum = (checksum * 31 + ord(ch)) % 1000000007
    print(f"{count} random mazes: the hole reached in {reached}, {letters} instructions in all, checksum {checksum}")


main()
