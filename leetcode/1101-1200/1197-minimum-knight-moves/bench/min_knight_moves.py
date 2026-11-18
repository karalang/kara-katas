# LeetCode #1197 bench: the ★ arm in Python, over the same 2000 random
# targets as the Kāra bench.
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


def main():
    seed = 1197

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    targets = []
    for _ in range(2000):
        s = next_random() % 301
        x = next_random() % (s + 1)
        y = s - x
        x = x if next_random() % 2 == 0 else -x
        y = y if next_random() % 2 == 0 else -y
        targets.append((x, y))
    check = 0
    for x, y in targets:
        m = min_knight_moves(x, y)
        check = (check * 131 + m + 1) % 1000000007
    print(f"2000 targets: checksum {check}")


main()
