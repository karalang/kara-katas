# LeetCode 749 — Contain Virus, bench: the ★ arm (flood fill each day)
# on a 50 x 50 grid that keeps changing. Mirrors contain_virus.kara.


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


seed = 749


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 3000
    grid = [[1 if next_random() % 100 < 5 else 0 for _ in range(50)] for _ in range(50)]
    total = 0
    check = 0
    for _ in range(rounds):
        for _ in range(20):
            r = next_random() % 50
            c = next_random() % 50
            grid[r][c] = 1 if next_random() % 100 < 5 else 0
        w = contain_virus(grid)
        total += w
        check = (check * 31 + w) % 1000000007
    print(f"{rounds} grids of 50 x 50: {total} walls in all, checksum {check}")


main()
