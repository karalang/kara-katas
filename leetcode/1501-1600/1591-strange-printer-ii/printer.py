# LeetCode #1591: Strange Printer II -- the Python mirror of printer.kara:
# each colour's bounding rectangle, the colours inside it printed later,
# and Kahn's algorithm for a cycle.


def is_printable(target_grid):
    rows = len(target_grid)
    cols = len(target_grid[0])
    top = [rows] * 61
    bottom = [-1] * 61
    left = [cols] * 61
    right = [-1] * 61
    for r in range(rows):
        for c in range(cols):
            k = target_grid[r][c]
            top[k] = min(top[k], r)
            bottom[k] = max(bottom[k], r)
            left[k] = min(left[k], c)
            right[k] = max(right[k], c)
    after = [[False] * 61 for _ in range(61)]
    before = [0] * 61
    for k in range(1, 61):
        for r in range(top[k], bottom[k] + 1):
            for c in range(left[k], right[k] + 1):
                other = target_grid[r][c]
                if other != k and not after[k][other]:
                    after[k][other] = True
                    before[other] += 1
    ready = [k for k in range(1, 61) if before[k] == 0]
    taken = 0
    while ready:
        k = ready.pop()
        taken += 1
        for other in range(1, 61):
            if after[k][other]:
                before[other] -= 1
                if before[other] == 0:
                    ready.append(other)
    return taken == 60


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def draw(rows, cols, colors, prints, rng):
    first = rng.next() % colors + 1
    grid = [[first] * cols for _ in range(rows)]
    for _ in range(1, prints):
        color = rng.next() % colors + 1
        r1 = rng.next() % rows
        r2 = rng.next() % rows
        c1 = rng.next() % cols
        c2 = rng.next() % cols
        for r in range(min(r1, r2), max(r1, r2) + 1):
            for c in range(min(c1, c2), max(c1, c2) + 1):
                grid[r][c] = color
    if rng.next() % 3 == 0:
        r = rng.next() % rows
        c = rng.next() % cols
        grid[r][c] = rng.next() % colors + 1
    return grid


def batch(count, most, colors, prints, rng):
    check = 0
    yes = 0
    for _ in range(count):
        rows = rng.next() % most + 1
        cols = rng.next() % most + 1
        grid = draw(rows, cols, colors, rng.next() % prints + 1, rng)
        ok = is_printable(grid)
        if ok:
            yes += 1
        check = mix(check, 1 if ok else 0)
    print(f"{count} grids of up to {most} by {most}, {colors} colours: {yes} printable, checksum {check}")


def main():
    examples = [
        [[1, 1, 1, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 1, 1, 1]],
        [[1, 1, 1, 1], [1, 1, 3, 3], [1, 1, 3, 4], [5, 5, 1, 4]],
        [[1, 2, 1], [2, 1, 2], [1, 2, 1]],
        [[7]],
        [[1, 2], [2, 1]],
        [[1, 1, 2], [3, 3, 2], [3, 3, 2]],
    ]
    for grid in examples:
        print(f"{grid} -> {'true' if is_printable(grid) else 'false'}")
    rng = Rng(1591)
    batch(3000, 4, 4, 5, rng)
    batch(300, 20, 20, 30, rng)
    batch(30, 60, 60, 80, rng)


main()
