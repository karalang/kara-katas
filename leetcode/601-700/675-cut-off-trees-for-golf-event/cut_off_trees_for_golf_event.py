# LeetCode #675: Cut Off Trees for Golf Event -- a breadth-first search
# for each walk.
# Mirrors the ★ arm (cut_off_trees_for_golf_event.kara) and its test
# harness.


def steps(forest, sr, sc, tr, tc):
    if sr == tr and sc == tc:
        return 0
    rows = len(forest)
    cols = len(forest[0])
    seen = [False] * (rows * cols)
    queue = [sr * cols + sc]
    seen[sr * cols + sc] = True
    head = 0
    dist = 0
    while head < len(queue):
        end = len(queue)
        dist += 1
        while head < end:
            cell = queue[head]
            head += 1
            r = cell // cols
            c = cell % cols
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols and forest[nr][nc] != 0 \
                        and not seen[nr * cols + nc]:
                    if nr == tr and nc == tc:
                        return dist
                    seen[nr * cols + nc] = True
                    queue.append(nr * cols + nc)
    return -1


def cut_off_tree(forest):
    trees = []
    for r in range(len(forest)):
        for c in range(len(forest[0])):
            if forest[r][c] > 1:
                trees.append((forest[r][c], r, c))
    trees.sort(key=lambda t: t[0])
    total = 0
    r = 0
    c = 0
    for _, tr, tc in trees:
        d = steps(forest, r, c, tr, tc)
        if d < 0:
            return -1
        total += d
        r = tr
        c = tc
    return total


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_forest(rng, rows, cols, walls, trees):
    forest = []
    spots = []
    for r in range(rows):
        row = []
        for c in range(cols):
            k = rng.next() % 100
            if (r > 0 or c > 0) and k < walls:
                row.append(0)
            else:
                row.append(1)
                if k < walls + trees:
                    spots.append(r * cols + c)
        forest.append(row)
    i = len(spots)
    while i > 1:
        j = rng.next() % i
        i -= 1
        spots[i], spots[j] = spots[j], spots[i]
    for k in range(len(spots)):
        forest[spots[k] // cols][spots[k] % cols] = 2 + k * 7
    return forest


def show(forest):
    if len(forest) * len(forest[0]) <= 12:
        rows = []
        for row in forest:
            rows.append("[" + ",".join(str(v) for v in row) + "]")
        return "[" + ",".join(rows) + "]"
    return f"{len(forest)}x{len(forest[0])}"


def main():
    cases = [
        [[1, 2, 3], [0, 0, 4], [7, 6, 5]],
        [[1, 2, 3], [0, 0, 0], [7, 6, 5]],
        [[2, 3, 4], [0, 0, 5], [8, 7, 6]],
        [[1]],
        [[5]],
        [[1, 1, 1, 9, 1, 1, 4]],
        [[1], [3], [0], [2]],
        [[3, 1, 2], [1, 0, 1], [4, 1, 5]],
        [[1, 1, 1], [1, 0, 1], [1, 1, 9]],
        [[1, 0, 1], [0, 1, 0], [1, 0, 2]],
    ]
    snake = []
    for r in range(50):
        row = []
        for c in range(50):
            if r % 2 == 1 and ((r % 4 == 1 and c < 49) or (r % 4 == 3 and c > 0)):
                row.append(0)
            else:
                row.append(1)
        snake.append(row)
    snake[49][49] = 1000000000
    snake[0][49] = 999999999
    cases.append(snake)
    rng = Rng(675)
    cases.append(random_forest(rng, 50, 50, 0, 15))
    cases.append(random_forest(rng, 50, 50, 12, 30))
    for forest in cases:
        print(f"{show(forest)}: {cut_off_tree(forest)}")
    s = 0
    reached = 0
    for c in range(200):
        rows = 1 + rng.next() % 20
        cols = 1 + rng.next() % 20
        walls = [0, 10, 25, 40][c % 4]
        forest = random_forest(rng, rows, cols, walls, 30)
        got = cut_off_tree(forest)
        if got >= 0:
            reached += 1
        s = (s * 31 + got + 1) % 1000000007
    print(f"200 random: {reached} reachable, checksum {s}")


main()
