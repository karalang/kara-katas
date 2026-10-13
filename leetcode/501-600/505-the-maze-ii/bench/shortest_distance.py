# Benchmark for #505 in Python: the ★ arm (Dijkstra over the cells the
# ball can stop in); see ../shortest_distance.kara. heapq is
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


seed = 505


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 2,000 mazes of 100 by 100 (the problem's most), a wall in each
    # cell with odds of 1 in 4, with a start and a destination in two
    # different open cells, built once. Then each is solved once.
    mazes = 2000
    all_mazes = []
    starts = []
    destinations = []
    for _ in range(mazes):
        maze = []
        open_cells = []
        for r in range(100):
            line = []
            for c in range(100):
                if next_random() % 4 == 0:
                    line.append(1)
                else:
                    line.append(0)
                    open_cells.append((r, c))
            maze.append(line)
        a = next_random() % len(open_cells)
        b = next_random() % (len(open_cells) - 1)
        if b >= a:
            b += 1
        starts.append([open_cells[a][0], open_cells[a][1]])
        destinations.append([open_cells[b][0], open_cells[b][1]])
        all_mazes.append(maze)
    reached = 0
    total = 0
    checksum = 0
    for k in range(mazes):
        d = shortest_distance(all_mazes[k], starts[k], destinations[k])
        if d != -1:
            reached += 1
            total += d
        checksum = (checksum * 31 + d + 1) % 1000000007
    print(f"{mazes} mazes of 100 by 100: the destination reached in {reached}, distance {total} in all, checksum {checksum}")


main()
