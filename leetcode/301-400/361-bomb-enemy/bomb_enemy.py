# LeetCode #361: Bomb Enemy -- mirror of bomb_enemy.kara.


def max_killed_enemies(grid):
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])
    best = 0
    row_hits = 0
    col_hits = [0] * cols
    for i in range(rows):
        for j in range(cols):
            if j == 0 or grid[i][j - 1] == "W":
                row_hits = 0
                k = j
                while k < cols and grid[i][k] != "W":
                    if grid[i][k] == "E":
                        row_hits += 1
                    k += 1
            if i == 0 or grid[i - 1][j] == "W":
                col_hits[j] = 0
                k = i
                while k < rows and grid[k][j] != "W":
                    if grid[k][j] == "E":
                        col_hits[j] += 1
                    k += 1
            if grid[i][j] == "0":
                best = max(best, row_hits + col_hits[j])
    return best


def show(label, grid):
    print(f"{label}: {max_killed_enemies(grid)}")


def main():
    show("example 1", ["0E00", "E0WE", "0E00"])
    show("example 2", ["WWW", "000", "EEE"])

    show("empty grid", [])
    show("one empty cell", ["0"])
    show("one enemy, nowhere to stand", ["E"])
    show("walls only", ["WW", "WW"])
    show("a wall shields", ["E0WE"])
    show("a column", ["E", "0", "E", "W", "E"])
    show("enemies everywhere but one cell", ["EEE", "E0E", "EEE"])
    show("the best cell is in a corner", ["0EE", "EWW", "EWE"])
    show("enemies do not block", ["0EEEE"])
    show("two segments in one row", ["0EWEE0"])

    seed = 361
    checksum = 0
    total = 0
    for _ in range(1000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        rows = (seed // 65536) % 8 + 1
        seed = (seed * 1103515245 + 12345) % 2147483648
        cols = (seed // 65536) % 8 + 1
        grid = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                seed = (seed * 1103515245 + 12345) % 2147483648
                r = (seed // 65536) % 6
                row.append("W" if r == 0 else "E" if r < 3 else "0")
            grid.append("".join(row))
        best = max_killed_enemies(grid)
        total += best
        checksum = (checksum * 31 + best) % 1000000007
    print(f"1000 random grids: {total} enemies in total, checksum {checksum}")


main()
