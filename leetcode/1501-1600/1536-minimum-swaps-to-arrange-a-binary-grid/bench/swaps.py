# LeetCode #1536: Minimum Swaps to Arrange a Binary Grid -- bench: the ★
# arm over 50 random 200 x 200 grids, built once and answered 50 times.
# Python mirror of swaps.kara.


def min_swaps(grid):
    n = len(grid)
    zeros = []
    for row in grid:
        count = 0
        while count < n and row[n - 1 - count] == 0:
            count += 1
        zeros.append(count)
    swaps = 0
    for i in range(n):
        need = n - 1 - i
        j = i
        while j < n and zeros[j] < need:
            j += 1
        if j == n:
            return -1
        while j > i:
            zeros[j], zeros[j - 1] = zeros[j - 1], zeros[j]
            j -= 1
            swaps += 1
    return swaps


seed = 1536


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def grid(n):
    zeros = list(range(n))
    if next_random() % 2 == 0:
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            zeros[i], zeros[j] = zeros[j], zeros[i]
        for i in range(n):
            zeros[i] = min(zeros[i] + next_random() % 2, n)
    else:
        for i in range(n):
            zeros[i] = next_random() % (n + 1)
    rows = []
    for i in range(n):
        row = [0] * n
        if zeros[i] < n:
            row[n - 1 - zeros[i]] = 1
            for c in range(n - 1 - zeros[i]):
                row[c] = next_random() % 2
        rows.append(row)
    return rows


grids = [grid(200) for _ in range(50)]
check = 0
for _ in range(50):
    for g in grids:
        check = mix(check, min_swaps(g) + 1)
print(f"50 passes over 50 grids of 200 rows: checksum {check}")
