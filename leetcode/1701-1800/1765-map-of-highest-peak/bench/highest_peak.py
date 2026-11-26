# LeetCode #1765: Map of Highest Peak -- the bench in Python, mirroring
# highest_peak.kara: a breadth-first search from every water cell at once.
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

seed = 1765
def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def main():
    size = 800
    grid = [[1 if next_random() % 5000 == 0 else 0 for _ in range(size)] for _ in range(size)]
    grid[0][0] = 1
    check = 0
    for call in range(100):
        r = (check + call * 7919) % size
        c = (check // 7 + call * 104729) % size
        grid[r][c] = 1 - grid[r][c]
        grid[0][0] = 1
        height = highest_peak(grid)
        check = (check * 31 + height[c][r] + height[size - 1 - r][size - 1 - c]) % 1000000007
    print(f"100 calls on 800 by 800: checksum {check}")

main()
