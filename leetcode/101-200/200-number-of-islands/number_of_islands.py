"""LeetCode 200 — Number of Islands (Python mirror / oracle).

Scan the grid; each unvisited land cell starts a new island, flood-filled to 0 via
an iterative stack of encoded row*cols+col positions. Mirrors the Kāra version.
"""


def num_islands(grid):
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                count += 1
                stack = [r * cols + c]
                grid[r][c] = 0
                while stack:
                    idx = stack.pop()
                    cr, cc = idx // cols, idx % cols
                    if cr > 0 and grid[cr - 1][cc] == 1:
                        grid[cr - 1][cc] = 0
                        stack.append((cr - 1) * cols + cc)
                    if cr + 1 < rows and grid[cr + 1][cc] == 1:
                        grid[cr + 1][cc] = 0
                        stack.append((cr + 1) * cols + cc)
                    if cc > 0 and grid[cr][cc - 1] == 1:
                        grid[cr][cc - 1] = 0
                        stack.append(cr * cols + (cc - 1))
                    if cc + 1 < cols and grid[cr][cc + 1] == 1:
                        grid[cr][cc + 1] = 0
                        stack.append(cr * cols + (cc + 1))
    return count


def report(grid):
    print(num_islands([row[:] for row in grid]))


def main():
    report([[1, 1, 1, 1, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 0], [0, 0, 0, 0, 0]])
    report([[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1]])
    report([[0, 0], [0, 0]])
    report([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    report([[1]])
    report([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


main()
