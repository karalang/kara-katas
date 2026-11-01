# LeetCode #1036: Escape a Large Maze -- bench
# Mirrors ./escape_maze.kara; see ../README.md § Benchmarks.
from collections import deque


def not_fenced(blocked, start, goal, side):
    limit = len(blocked) * (len(blocked) - 1) // 2
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal or len(seen) > limit:
            return True
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nxt = (x + dx, y + dy)
            nx, ny = nxt
            if 0 <= nx < side and 0 <= ny < side and nxt not in blocked and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


def escape_within(blocked, source, target, side):
    walls = set(blocked)
    return not_fenced(walls, source, target, side) and not_fenced(walls, target, source, side)


def is_escape_possible(blocked, source, target):
    return escape_within(blocked, source, target, 1000000)



def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rounds = 4
    seed = [1036]
    mazes = []
    for k in range(30):
        blocked = []
        cx = next_random(seed) % 900000 + 50000
        cy = next_random(seed) % 900000 + 50000
        if k % 3 == 2:
            blocked = [(i, 199 - i) for i in range(200)]
            mazes.append((blocked, (200, 0), (cx, cy)))
        else:
            for i in range(50):
                blocked += [(cx + i, cy + 50 - i), (cx + 50 - i, cy - i), (cx - i, cy - 50 + i), (cx - 50 + i, cy + i)]
            if k % 3 == 0:
                mazes.append((blocked, (cx + 10, cy - 10), (0, 0)))
            else:
                mazes.append((blocked, (cx + 60, cy), (999999, 999999)))
    escapes = 0
    check = 0
    for _ in range(rounds):
        for blocked, source, target in mazes:
            answer = is_escape_possible(blocked, source, target)
            if answer:
                escapes += 1
            check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"30 mazes of 200 blocks, {rounds} rounds: {escapes} escapes, checksum {check}")


main()
