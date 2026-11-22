# LeetCode #2711: Difference of Number of Distinct Values on Diagonals --
# the bench (diagonals.kara in Python): each diagonal swept down and then
# up with a table of the values seen.


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


count, rounds = 2000, 5
grids = []
for _ in range(count):
    cap = next_random() % 50 + 1
    grids.append([[next_random() % cap + 1 for _ in range(50)] for _ in range(50)])
total = 0
check = 0
for r in range(rounds):
    for grid in grids:
        for row in difference_of_distinct_values(grid):
            for v in row:
                total += v
                check = (check * 31 + v) % 1000000007
        check = (check + r) % 1000000007
print(f"{count} grids of 50 by 50, {rounds} rounds: differences sum to {total}, checksum {check}")
