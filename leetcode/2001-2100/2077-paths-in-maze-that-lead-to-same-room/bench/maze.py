# LeetCode #2077: Paths in Maze That Lead to Same Room -- Python mirror of
# the ★ arm's benchmark (maze.kara): 30 mazes of 1000 rooms and about
# 38000 corridors; each room's rooms above it a set, and every corridor's
# triangles the size of its two rooms' sets' intersection.


def number_of_paths(n, corridors):
    up = [set() for _ in range(n + 1)]
    for c in corridors:
        a, b = min(c), max(c)
        up[a].add(b)
    count = 0
    for a in range(1, n + 1):
        for b in up[a]:
            count += len(up[a] & up[b])
    return count


seed = 2077


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_maze(n, count, near):
    seen = set()
    corridors = []
    for _ in range(count):
        a = next_random() % n + 1
        step = next_random() % min(near, n - 1) + 1
        b = (a - 1 + step) % n + 1
        key = min(a, b) * 100000 + max(a, b)
        if key not in seen:
            seen.add(key)
            corridors.append([a, b] if next_random() % 2 == 0 else [b, a])
    return corridors


total = 0
check = 0
for _ in range(30):
    corridors = random_maze(1000, 60000, 60)
    a = number_of_paths(1000, corridors)
    total += a
    check = (check * 31 + a) % 1000000007
print(f"30 mazes: sum {total}, checksum {check}")
