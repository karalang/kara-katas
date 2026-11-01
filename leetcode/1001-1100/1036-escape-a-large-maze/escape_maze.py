# LeetCode #1036: Escape a Large Maze -- Python mirror of escape_maze.kara
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


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(b):
    return "true" if b else "false"


def main():
    corner = [(k, 199 - k) for k in range(200)]
    diamond = []
    for k in range(50):
        diamond.append((500000 + k, 500000 + 50 - k))
        diamond.append((500000 + 50 - k, 500000 - k))
        diamond.append((500000 - k, 500000 - 50 + k))
        diamond.append((500000 - 50 + k, 500000 + k))
    examples = [
        ("two blocks round a corner", [(0, 1), (1, 0)], (0, 0), (0, 2)),
        ("no blocks", [], (0, 0), (999999, 999999)),
        ("two blocks, target in the corner", [(0, 1), (1, 0)], (0, 2), (0, 0)),
        ("a wall of 200 across a corner, from inside", corner, (0, 0), (500, 500)),
        ("a wall of 200 across a corner, from the last square inside", corner, (198, 0), (199, 1)),
        ("a wall of 200 across a corner, both inside", corner, (0, 0), (0, 198)),
        ("a wall of 200 across a corner, both outside", corner, (199, 1), (999999, 0)),
        ("a diamond of 200, from the centre", diamond, (500000, 500000), (0, 0)),
        ("a diamond of 200, to the centre", diamond, (999999, 999999), (500000, 500000)),
        ("a diamond of 200, both inside", diamond, (500000, 500000), (500049, 500000)),
        ("a diamond of 200, just outside", diamond, (500000, 500051), (0, 999999)),
    ]
    for name, blocked, source, target in examples:
        print(f"{name}: {show(is_escape_possible(blocked, source, target))}")
    seed = [1036]
    for count, blocks, spread in [(40, 10, 6), (40, 50, 12), (20, 200, 25), (20, 200, 1000000)]:
        free = 0
        check = 0
        for _ in range(count):
            base = 0 if next_random(seed) % 2 == 0 else 1000000 - spread
            taken = set()
            blocked = []
            while len(blocked) < blocks:
                cell = (base + next_random(seed) % spread, base + next_random(seed) % spread)
                if cell not in taken:
                    taken.add(cell)
                    blocked.append(cell)
            ends = []
            while len(ends) < 2:
                cell = (base + next_random(seed) % spread, base + next_random(seed) % spread)
                if cell not in taken:
                    taken.add(cell)
                    ends.append(cell)
            answer = is_escape_possible(blocked, ends[0], ends[1])
            if answer:
                free += 1
            check = (check * 131 + (2 if answer else 1)) % 1000000007
        print(f"{count} mazes of {blocks} blocks within {spread} of a corner: {free} escape, checksum {check}")


main()
