# LeetCode #711: Number of Distinct Islands II -- canonical forms
# counted by sorting.
# Benchmark mirror of the Kara sorted arm: each island by depth-first
# search with a stack; its canonical form the smallest of its eight
# symmetries, sorted and moved to the origin; forms sorted and counted.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def canonical(cells):
    best = None
    for k in range(8):
        moved = []
        for r, c in cells:
            a, b = (r, c) if k < 4 else (c, r)
            x = -a if k % 2 == 1 else a
            y = -b if k % 4 >= 2 else b
            moved.append((x, y))
        moved.sort()
        r0, c0 = moved[0]
        flat = []
        for r, c in moved:
            flat.append(r - r0)
            flat.append(c - c0)
        if k == 0 or flat < best:
            best = flat
    return best


def num_distinct_islands2(grid):
    rows, cols = len(grid), len(grid[0])
    seen = [False] * (rows * cols)
    forms = []
    for start in range(rows * cols):
        if grid[start // cols][start % cols] == 0 or seen[start]:
            continue
        cells = []
        stack = [start]
        seen[start] = True
        while stack:
            at = stack.pop()
            r, c = divmod(at, cols)
            cells.append((r, c))
            if r > 0 and grid[r - 1][c] == 1 and not seen[at - cols]:
                seen[at - cols] = True
                stack.append(at - cols)
            if r + 1 < rows and grid[r + 1][c] == 1 and not seen[at + cols]:
                seen[at + cols] = True
                stack.append(at + cols)
            if c > 0 and grid[r][c - 1] == 1 and not seen[at - 1]:
                seen[at - 1] = True
                stack.append(at - 1)
            if c + 1 < cols and grid[r][c + 1] == 1 and not seen[at + 1]:
                seen[at + 1] = True
                stack.append(at + 1)
        forms.append(canonical(cells))
    forms.sort()
    count = 0
    for i in range(len(forms)):
        if i == 0 or forms[i] != forms[i - 1]:
            count += 1
    return count


def main():
    seed = [711]
    grids = []
    for g in range(100):
        pct = 30 + g * 2 // 5
        grids.append([[1 if next_random(seed) % 100 < pct else 0
                       for _ in range(50)] for _ in range(50)])
    total = 0
    for _ in range(10):
        for grid in grids:
            total += num_distinct_islands2(grid)
    print(f"10 rounds of 100 grids of 50 by 50: {total} distinct islands")


main()
