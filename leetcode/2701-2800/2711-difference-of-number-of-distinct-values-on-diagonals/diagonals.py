# LeetCode #2711: Difference of Number of Distinct Values on Diagonals --
# the Python mirror of the star arm (diagonals.kara): each diagonal swept
# down once and up once with a count of each value, the distinct values
# above each cell written down on the way down and the ones below
# subtracted on the way up.


def difference_of_distinct_values(grid):
    m = len(grid)
    n = len(grid[0])
    answer = [[0] * n for _ in range(m)]
    starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
    for r0, c0 in starts:
        length = min(m - r0, n - c0)
        seen = [False] * 51
        distinct = 0
        for k in range(length):
            answer[r0 + k][c0 + k] = distinct
            v = grid[r0 + k][c0 + k]
            if not seen[v]:
                seen[v] = True
                distinct += 1
        seen = [False] * 51
        distinct = 0
        for k in range(length - 1, -1, -1):
            answer[r0 + k][c0 + k] = abs(answer[r0 + k][c0 + k] - distinct)
            v = grid[r0 + k][c0 + k]
            if not seen[v]:
                seen[v] = True
                distinct += 1
    return answer


seed = 2711


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(grid):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in grid) + "]"


def fold(check, grid):
    for row in grid:
        for v in row:
            check = (check * 31 + v) % 1000000007
    return (check * 31 + len(grid) * 100 + len(grid[0])) % 1000000007


print(show(difference_of_distinct_values([[1, 2, 3], [3, 1, 5], [3, 2, 1]])))
print(show(difference_of_distinct_values([[1]])))
print(show(difference_of_distinct_values([[1, 2, 3, 4, 5]])))
print(show(difference_of_distinct_values([[7], [7], [8]])))
print(show(difference_of_distinct_values([[(r + c) % 2 + 1 for c in range(4)] for r in range(4)])))
big = difference_of_distinct_values([[(r * 50 + c) % 50 + 1 for c in range(50)] for r in range(50)])
print(f"50 by 50, all distinct along diagonals: corner {big[0][0]}, centre {big[25][25]}, sum {sum(map(sum, big))}")
total = 0
check = 0
for _ in range(1000):
    m = next_random() % 50 + 1
    n = next_random() % 50 + 1
    most = next_random() % 50 + 1
    grid = [[next_random() % most + 1 for _ in range(n)] for _ in range(m)]
    answer = difference_of_distinct_values(grid)
    total += sum(map(sum, answer))
    check = fold(check, answer)
print(f"1000 grids: differences sum to {total}, checksum {check}")
