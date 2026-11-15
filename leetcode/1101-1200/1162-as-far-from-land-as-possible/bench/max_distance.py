# LeetCode #1162: As Far from Land as Possible -- Python mirror of the Kāra
# ★ arm: a breadth-first search from every land cell at once, over a flat
# distance array and a queue of cell indices.


def max_distance(grid):
    n = len(grid)
    dist = [-1] * (n * n)
    queue = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                dist[i * n + j] = 0
                queue.append(i * n + j)
    if len(queue) == 0 or len(queue) == n * n:
        return -1
    head = 0
    far = 0
    while head < len(queue):
        cell = queue[head]
        head += 1
        i, j = cell // n, cell % n
        far = dist[cell]
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            a, b = i + di, j + dj
            if 0 <= a < n and 0 <= b < n and dist[a * n + b] < 0:
                dist[a * n + b] = far + 1
                queue.append(a * n + b)
    return far


seed = 1162


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    odds = [1, 2, 5, 10, 50, 200, 500, 900]
    grids = []
    for k in range(16):
        o = odds[k % 8]
        grids.append([[1 if next_random() % 1000 < o else 0 for _ in range(100)] for _ in range(100)])
    total = 0
    check = 0
    for _ in range(300):
        for k in range(16):
            a = next_random() % 100
            b = next_random() % 100
            grids[k][a][b] = 1 - grids[k][a][b]
            d = max_distance(grids[k])
            total += d
            check = (check * 31 + d + 1) % 1000000007
    print(f"300 rounds over 16 grids of 100 by 100: total {total}, checksum {check}")


main()
