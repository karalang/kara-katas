# LeetCode 749 — Contain Virus, flood fill each day.
# Mirror of contain_virus.kara (the ★ arm); same output, byte for byte.


def contain_virus(is_infected):
    m, n = len(is_infected), len(is_infected[0])
    g = [v for row in is_infected for v in row]
    walls = 0
    while True:
        region = [-1] * (m * n)
        mark = [-1] * (m * n)
        cells, threats, needs = [], [], []
        for start in range(m * n):
            if g[start] != 1 or region[start] != -1:
                continue
            rid = len(cells)
            mine, threat, need = [], [], 0
            stack = [start]
            region[start] = rid
            while stack:
                at = stack.pop()
                mine.append(at)
                r, c = divmod(at, n)
                nxt = []
                if r > 0:
                    nxt.append(at - n)
                if r < m - 1:
                    nxt.append(at + n)
                if c > 0:
                    nxt.append(at - 1)
                if c < n - 1:
                    nxt.append(at + 1)
                for y in nxt:
                    if g[y] == 0:
                        need += 1
                        if mark[y] != rid:
                            mark[y] = rid
                            threat.append(y)
                    elif g[y] == 1 and region[y] == -1:
                        region[y] = rid
                        stack.append(y)
            cells.append(mine)
            threats.append(threat)
            needs.append(need)
        best = -1
        for rid in range(len(cells)):
            if threats[rid] and (best == -1 or len(threats[rid]) > len(threats[best])):
                best = rid
        if best == -1:
            break
        walls += needs[best]
        for rid in range(len(cells)):
            if rid == best:
                for x in cells[rid]:
                    g[x] = 2
            else:
                for x in threats[rid]:
                    g[x] = 1
    return walls


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(text):
    grid = [[1 if c == '1' else 0 for c in row] for row in text.split('/')]
    print(f"{text} -> {contain_virus(grid)}")


def random_grid(rng, m, n, percent):
    return [[1 if rng.next() % 100 < percent else 0 for _ in range(n)] for _ in range(m)]


def main():
    for t in ["01000001/01000001/00000001/00000000", "111/101/111",
              "111000000/101011111/111000000", "0", "1", "10", "1111/1111",
              "1000/0000/0000/0001", "10101/01010/10101", "00000/00100/00000"]:
        show(t)
    rng = Rng(749)
    for percent in [1, 3, 10, 30]:
        grid = random_grid(rng, 50, 50, percent)
        print(f"50 x 50, {percent}% infected: {contain_virus(grid)} walls")
    total = 0
    check = 0
    for _ in range(300):
        m = 1 + rng.next() % 8
        n = 1 + rng.next() % 8
        percent = 5 + rng.next() % 40
        grid = random_grid(rng, m, n, percent)
        w = contain_virus(grid)
        total += w
        check = (check * 31 + w) % 1000000007
    print(f"300 random grids: {total} walls in all, checksum {check}")


main()
