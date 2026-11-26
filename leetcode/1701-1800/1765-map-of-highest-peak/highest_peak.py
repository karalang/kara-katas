# LeetCode #1765: Map of Highest Peak -- the ★ arm in Python: a
# breadth-first search from every water cell at once.
from collections import deque

def highest_peak(is_water):
    rows, cols = len(is_water), len(is_water[0])
    height = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if is_water[r][c] == 1:
                height[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and height[nr][nc] == -1:
                height[nr][nc] = height[r][c] + 1
                queue.append((nr, nc))
    return height

seed = 0
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_grid(rows, cols, water):
    grid = [[1 if next_random() % 1000 < water else 0 for _ in range(cols)] for _ in range(rows)]
    if all(v == 0 for row in grid for v in row):
        r = next_random() % rows
        c = next_random() % cols
        grid[r][c] = 1
    return grid

def digest(height):
    check = 0
    for row in height:
        for v in row:
            check = (check * 31 + v) % 1000000007
    return check

def show(h):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in h) + "]"

def main():
    global seed
    print(show(highest_peak([[0, 1], [0, 0]])), show(highest_peak([[0, 0, 1], [1, 0, 0], [0, 0, 0]])))
    print(" ".join(show(highest_peak(g)) for g in [[[1]], [[1, 0, 0, 0]], [[0], [0], [1]], [[1, 1], [1, 1]], [[1, 0, 0], [0, 0, 0], [0, 0, 1]]]))
    seed = 1765
    corner = [[0] * 1000 for _ in range(1000)]
    corner[0][0] = 1
    lakes = random_grid(1000, 1000, 10)
    a = highest_peak(corner)
    b = highest_peak(lakes)
    print(f"the most: {max(map(max, a))} {digest(a)}, {max(map(max, b))} {digest(b)}")
    check = 0
    for _ in range(3000):
        rows = 1 + next_random() % 8
        cols = 1 + next_random() % 8
        water = 1 + next_random() % 500
        grid = random_grid(rows, cols, water)
        check = (check * 31 + digest(highest_peak(grid))) % 1000000007
    print(f"3000 random grids: checksum {check}")

main()
