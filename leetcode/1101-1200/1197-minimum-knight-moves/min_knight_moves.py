# LeetCode #1197: Minimum Knight Moves -- the ★ arm in Python: the target
# folded into the first quadrant, and a breadth-first search from the origin
# over the squares from -2 to 302 in each coordinate.
from collections import deque

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def min_knight_moves(x, y):
    tx, ty = abs(x), abs(y)
    side = 305
    seen = [False] * (side * side)
    queue = deque([(0, 0, 0)])
    seen[2 * side + 2] = True
    while queue:
        cx, cy, steps = queue.popleft()
        if cx == tx and cy == ty:
            return steps
        for dx, dy in MOVES:
            nx, ny = cx + dx, cy + dy
            if -2 <= nx <= 302 and -2 <= ny <= 302:
                k = (nx + 2) * side + ny + 2
                if not seen[k]:
                    seen[k] = True
                    queue.append((nx, ny, steps + 1))
    return -1


# ---- test harness ---------------------------------------------------------

seed = 1197


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [(2, 1), (5, 5), (0, 0), (1, 0), (1, 1), (2, 2), (-1, -2), (0, -1), (3, 0), (300, 0), (0, -300), (150, 150), (-150, 150), (1, 299)]
    for x, y in cases:
        print(f"({x}, {y}): {min_knight_moves(x, y)}")
    total = 0
    check = 0
    for _ in range(100):
        s = next_random() % 301
        x = next_random() % (s + 1)
        y = s - x
        x = x if next_random() % 2 == 0 else -x
        y = y if next_random() % 2 == 0 else -y
        m = min_knight_moves(x, y)
        total += m
        check = (check * 131 + m + 1) % 1000000007
    print(f"100 random targets: {total} moves, checksum {check}")


main()
