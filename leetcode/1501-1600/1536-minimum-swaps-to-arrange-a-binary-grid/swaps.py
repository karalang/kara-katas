# LeetCode #1536: Minimum Swaps to Arrange a Binary Grid -- Python mirror
# of swaps.kara (greedy over the rows' trailing zeros); output
# byte-identical.


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


def batch(count, most):
    check = 0
    solvable = 0
    for _ in range(count):
        n = next_random() % most + 1
        answer = min_swaps(grid(n))
        if answer >= 0:
            solvable += 1
        check = mix(check, answer + 1)
    print(f"{count} grids of 1 to {most} rows: {solvable} solvable, checksum {check}")


def show(g):
    return "[" + ", ".join("[" + ", ".join(map(str, r)) + "]" for r in g) + "]"


for g in [[[0, 0, 1], [1, 1, 0], [1, 0, 0]], [[0, 1, 1, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 1, 1, 0]],
          [[1, 0, 0], [1, 1, 0], [1, 1, 1]], [[1]], [[1, 1], [1, 0]], [[1, 1], [0, 1]]]:
    print(f"{show(g)} -> {min_swaps(g)}")
n = 200
rev = []
for i in range(n):
    row = [0] * n
    row[n - 1 - i] = 1
    rev.append(row)
print(f"200 rows reversed -> {min_swaps(rev)}")
batch(3000, 8)
batch(300, 200)
