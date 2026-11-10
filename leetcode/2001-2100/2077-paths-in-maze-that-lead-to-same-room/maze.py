# LeetCode #2077: Paths in Maze That Lead to Same Room -- Python mirror of
# the ★ arm (maze.kara): every corridor led from the lower room to the
# higher, the rooms above each room a set, and a corridor's triangles the
# size of its two rooms' sets' intersection.


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


def show(corridors):
    return "[" + ",".join(f"[{c[0]},{c[1]}]" for c in corridors) + "]"


examples = [
    (5, [[1, 2], [5, 2], [4, 1], [2, 4], [3, 1], [3, 4]]),
    (4, [[1, 2], [3, 4]]),
    (3, [[1, 2], [2, 3], [3, 1]]),
    (2, [[1, 2]]),
    (4, [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]),
    (5, [[1, 2], [2, 3], [3, 4], [4, 5], [5, 1]]),
    (6, [[6, 1], [1, 5], [5, 6], [2, 3], [3, 4], [4, 2], [1, 2]]),
]
for n, corridors in examples:
    print(f"n = {n}, {show(corridors)} -> {number_of_paths(n, corridors)}")
total = 0
check = 0
for _ in range(300):
    n = next_random() % 59 + 2
    count = next_random() % 201
    near = [3, 10, 60][next_random() % 3]
    corridors = random_maze(n, count, near)
    a = number_of_paths(n, corridors)
    total += a
    check = (check * 31 + a) % 1000000007
print(f"300 mazes: sum {total}, checksum {check}")
corridors = random_maze(1000, 60000, 60)
print(f"1000 rooms, {len(corridors)} corridors -> {number_of_paths(1000, corridors)}")
