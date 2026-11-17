# LeetCode #1594: Maximum Non Negative Product in a Matrix -- mirrors product.kara.


def max_product_path(grid):
    rows, cols = len(grid), len(grid[0])
    hi = [[0] * cols for _ in range(rows)]
    lo = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            v = grid[r][c]
            if r == 0 and c == 0:
                hi[r][c] = lo[r][c] = v
                continue
            best, worst = None, None
            for pr, pc in ((r - 1, c), (r, c - 1)):
                if pr < 0 or pc < 0:
                    continue
                for x in (hi[pr][pc] * v, lo[pr][pc] * v):
                    best = x if best is None else max(best, x)
                    worst = x if worst is None else min(worst, x)
            hi[r][c], lo[r][c] = best, worst
    top = hi[rows - 1][cols - 1]
    return -1 if top < 0 else top % 1000000007


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, seed):
    check = 0
    negative = 0
    for _ in range(count):
        rows = next_random(seed) % most + 1
        cols = next_random(seed) % most + 1
        grid = [[next_random(seed) % 9 - 4 for _ in range(cols)] for _ in range(rows)]
        answer = max_product_path(grid)
        if answer == -1:
            negative += 1
        check = mix(check, answer)
    print(f"{count} grids of up to {most} by {most}: {negative} only negative, checksum {check}")


def show(grid):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in grid) + "]"


def main():
    examples = [
        [[-1, -2, -3], [-2, -3, -3], [-3, -3, -2]],
        [[1, -2, 1], [1, -2, 1], [3, -4, 1]],
        [[1, 3], [0, -4]],
        [[-4]],
        [[0]],
        [[4] * 15 for _ in range(15)],
        [[-4] * 15 for _ in range(15)],
    ]
    for grid in examples:
        shown = f"[[{grid[0][0]}; 15]; 15]" if len(grid) > 4 else show(grid)
        print(f"{shown} -> {max_product_path(grid)}")
    seed = [1594]
    batch(3000, 4, seed)
    batch(300, 15, seed)


main()
