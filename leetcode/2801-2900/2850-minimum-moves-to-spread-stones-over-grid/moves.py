# LeetCode #2850: Minimum Moves to Spread Stones Over Grid -- the Python
# mirror of the ★ arm: the empty cells given to the spare stones in
# every way by backtracking, each stone's moves the cells' distance.


def spread(k, frm, to, used):
    if k == len(frm):
        return 0
    r, c = frm[k]
    best = 2**63 - 1
    for j in range(len(to)):
        if not used[j]:
            used[j] = True
            tr, tc = to[j]
            best = min(best, abs(r - tr) + abs(c - tc) + spread(k + 1, frm, to, used))
            used[j] = False
    return best


def minimum_moves(grid):
    frm, to = [], []
    for r in range(3):
        for c in range(3):
            if grid[r][c] == 0:
                to.append((r, c))
            for _ in range(1, grid[r][c]):
                frm.append((r, c))
    return spread(0, frm, to, [False] * len(to))


def every(cell, left, counts, out):
    if cell == 8:
        counts[8] = left
        out.append([[counts[r * 3 + c] for c in range(3)] for r in range(3)])
        return
    for k in range(left + 1):
        counts[cell] = k
        every(cell + 1, left - k, counts, out)


def main():
    print(minimum_moves([[1, 1, 0], [1, 1, 1], [1, 2, 1]]), minimum_moves([[1, 3, 0], [1, 0, 0], [1, 0, 3]]))
    print(minimum_moves([[1, 1, 1], [1, 1, 1], [1, 1, 1]]), minimum_moves([[9, 0, 0], [0, 0, 0], [0, 0, 0]]),
          minimum_moves([[0, 0, 0], [0, 9, 0], [0, 0, 0]]))
    grids = []
    every(0, 9, [0] * 9, grids)
    total = most = check = 0
    for grid in grids:
        moves = minimum_moves(grid)
        total += moves
        most = max(most, moves)
        check = (check * 31 + moves) % 1000000007
    print(f"{len(grids)} grids: {total} moves in all, at most {most}, checksum {check}")


main()
