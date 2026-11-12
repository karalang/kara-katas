# LeetCode #1139: Largest 1-Bordered Square -- the bench, the ★ arm's
# algorithm: runs of 1s left and up, each corner's sides tried from the longest down.


def largest1_bordered_square(grid):
    rows, cols = len(grid), len(grid[0])
    left = [[0] * cols for _ in range(rows)]
    up = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                left[i][j] = left[i][j - 1] + 1 if j > 0 else 1
                up[i][j] = up[i - 1][j] + 1 if i > 0 else 1
    best = 0
    for i in range(rows):
        for j in range(cols):
            k = min(left[i][j], up[i][j])
            while k > best:
                if left[i - k + 1][j] >= k and up[i][j - k + 1] >= k:
                    best = k
                k -= 1
    return best * best


seed = 1139


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grids = [[[1 if next_random() % 100 < 95 else 0 for _ in range(100)] for _ in range(100)] for _ in range(20)]
    total = 0
    check = 0
    for _ in range(300):
        for g in range(20):
            i = next_random() % 100
            j = next_random() % 100
            grids[g][i][j] = 1 - grids[g][i][j]
            area = largest1_bordered_square(grids[g])
            total += area
            check = (check * 131 + area + 1) % 1000000007
    print(f"300 rounds over 20 grids of 100 by 100: areas total {total}, checksum {check}")


main()
