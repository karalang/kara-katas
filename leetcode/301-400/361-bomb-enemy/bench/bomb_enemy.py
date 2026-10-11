# Benchmark for #361 -- mirror of bomb_enemy.kara.


def max_killed_enemies(grid):
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])
    best = 0
    row_hits = 0
    col_hits = [0] * cols
    for i in range(rows):
        line = grid[i]
        for j in range(cols):
            if j == 0 or line[j - 1] == "W":
                row_hits = 0
                k = j
                while k < cols and line[k] != "W":
                    if line[k] == "E":
                        row_hits += 1
                    k += 1
            if i == 0 or grid[i - 1][j] == "W":
                col_hits[j] = 0
                k = i
                while k < rows and grid[k][j] != "W":
                    if grid[k][j] == "E":
                        col_hits[j] += 1
                    k += 1
            if line[j] == "0":
                best = max(best, row_hits + col_hits[j])
    return best


def main():
    seed = 361
    total = 0
    checksum = 0
    for _ in range(60):
        grid = []
        for _ in range(400):
            row = []
            for _ in range(400):
                seed = (seed * 1103515245 + 12345) % 2147483648
                r = (seed // 65536) % 6
                row.append("W" if r == 0 else "E" if r < 3 else "0")
            grid.append("".join(row))
        best = max_killed_enemies(grid)
        total += best
        checksum = (checksum * 31 + best) % 1000000007
    print(f"60 grids: {total} enemies in total, checksum {checksum}")


main()
