# Benchmark for #499: Python mirror of the ★ arm (Dijkstra over the
# places the ball stops); see the_maze_iii.kara.
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


seed = 499


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 1,000 mazes of 100 by 100 (the problem's most), a wall in each
    # cell with odds of 1 in 4, with a ball and a hole in two different
    # open cells, built once. Then each is solved once.
    mazes = 1000
    all_mazes = []
    balls = []
    holes = []
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
        balls.append([open_cells[a][0], open_cells[a][1]])
        holes.append([open_cells[b][0], open_cells[b][1]])
        all_mazes.append(maze)
    reached = 0
    letters = 0
    checksum = 0
    for k in range(mazes):
        way = find_shortest_way(all_mazes[k], balls[k], holes[k])
        if way != "impossible":
            reached += 1
            letters += len(way)
        for ch in way:
            checksum = (checksum * 31 + ord(ch)) % 1000000007
    print(f"{mazes} mazes of 100 by 100: the hole reached in {reached}, {letters} instructions in all, checksum {checksum}")


main()
