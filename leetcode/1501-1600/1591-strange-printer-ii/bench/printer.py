# LeetCode #1591: Strange Printer II -- the bench in Python, mirroring
# printer.kara:
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


def main():
    rng = Rng(1591)
    grids = []
    for g in range(4000):
        order = list(range(1, 61))
        for i in range(59, 0, -1):
            j = rng.next() % (i + 1)
            order[i], order[j] = order[j], order[i]
        grid = [[order[0]] * 60 for _ in range(60)]
        for k in order[1:]:
            r1 = rng.next() % 60
            r2 = rng.next() % 60
            c1 = rng.next() % 60
            c2 = rng.next() % 60
            for r in range(min(r1, r2), max(r1, r2) + 1):
                for c in range(min(c1, c2), max(c1, c2) + 1):
                    grid[r][c] = k
        if g % 2 == 1:
            r = rng.next() % 60
            c = rng.next() % 60
            grid[r][c] = rng.next() % 60 + 1
        grids.append(grid)
    check = 0
    yes = 0
    for grid in grids:
        ok = is_printable(grid)
        if ok:
            yes += 1
        check = mix(check, 1 if ok else 0)
    print(f"4000 grids of 60 by 60: {yes} printable, checksum {check}")


main()
