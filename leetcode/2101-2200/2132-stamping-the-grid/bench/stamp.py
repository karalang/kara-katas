# LeetCode #2132: Stamping the Grid -- the benchmark, the same algorithm
# as stamp.kara.


def possible_to_stamp(grid, stamp_height, stamp_width):
    m = len(grid)
    n = len(grid[0])
    w = n + 1
    full = [0] * ((m + 1) * w)
    for r in range(m):
        for c in range(n):
            full[(r + 1) * w + c + 1] = grid[r][c] + full[r * w + c + 1] + full[(r + 1) * w + c] - full[r * w + c]
    marks = [0] * ((m + 1) * w)
    for r in range(m - stamp_height + 1):
        for c in range(n - stamp_width + 1):
            r2 = r + stamp_height
            c2 = c + stamp_width
            if full[r2 * w + c2] - full[r * w + c2] - full[r2 * w + c] + full[r * w + c] == 0:
                marks[r * w + c] += 1
                marks[r * w + c2] -= 1
                marks[r2 * w + c] -= 1
                marks[r2 * w + c2] += 1
    for r in range(m):
        for c in range(n):
            if r > 0:
                marks[r * w + c] += marks[(r - 1) * w + c]
            if c > 0:
                marks[r * w + c] += marks[r * w + c - 1]
            if r > 0 and c > 0:
                marks[r * w + c] -= marks[(r - 1) * w + c - 1]
            if grid[r][c] == 0 and marks[r * w + c] == 0:
                return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2132]
    grid = [[1 if r % 4 == 3 or c % 4 == 3 else 0 for c in range(500)] for r in range(400)]
    stamped = 0
    check = 0
    for rnd in range(100):
        hi = next_random(seed)
        at = (hi * 32768 + next_random(seed)) % 200000
        r, c = at // 500, at % 500
        grid[r][c] = 1 - grid[r][c]
        h = next_random(seed) % 3 + 1
        w = next_random(seed) % 3 + 1
        fits = 1 if possible_to_stamp(grid, h, w) else 0
        grid[r][c] = 1 - grid[r][c]
        stamped += fits
        check = (check * 31 + fits + at + rnd) % 1000000007
    print(f"100 solves: {stamped} stamped, checksum {check}")


main()
