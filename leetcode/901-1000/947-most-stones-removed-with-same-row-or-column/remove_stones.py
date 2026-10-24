# LeetCode #947: Most Stones Removed with Same Row or Column -- rows and
# columns joined.
# Mirrors remove_stones.kara (the ★ arm) and its harness.


def find_line(parent, v):
    x = v
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def remove_stones(stones):
    parent = [-1] * 20002
    for s in stones:
        row = s[0]
        col = 10001 + s[1]
        if parent[row] < 0:
            parent[row] = row
        if parent[col] < 0:
            parent[col] = col
        a = find_line(parent, row)
        b = find_line(parent, col)
        if a != b:
            parent[a] = b
    groups = 0
    for v in range(20002):
        if parent[v] == v:
            groups += 1
    return len(stones) - groups


seed = 947


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(stones):
    return "[" + ",".join(f"[{s[0]},{s[1]}]" for s in stones) + "]"


def removed_text(r):
    return "1 stone removed" if r == 1 else f"{r} stones removed"


def random_stones(n, w, h):
    taken = set()
    stones = []
    want = min(n, w * h)
    while len(stones) < want:
        x = (next_random() * 32768 + next_random()) % w
        y = (next_random() * 32768 + next_random()) % h
        if x * 10001 + y not in taken:
            taken.add(x * 10001 + y)
            stones.append([x, y])
    return stones


def main():
    examples = [
        [[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]],
        [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]],
        [[0, 0]],
        [[0, 0], [0, 5]],
        [[0, 0], [1, 1], [2, 2], [3, 3]],
        [[0, 0], [0, 1], [1, 1], [1, 2], [2, 2]],
        [[10000, 10000], [10000, 0], [0, 10000]],
        [[0, 0], [0, 1], [5, 5], [5, 6], [9, 0]],
    ]
    for stones in examples:
        print(f"{show(stones)}: {removed_text(remove_stones(stones))}")
    count = 0
    removed = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 40
        w = 1 + next_random() % 25
        h = 1 + next_random() % 25
        stones = random_stones(n, w, h)
        r = remove_stones(stones)
        count += len(stones)
        removed += r
        check = (check * 31 + r) % 1000000007
    print(f"300 random sets of {count} stones: {removed} removed, checksum {check}")
    wide = random_stones(1000, 10001, 10001)
    print(f"1000 stones at random points up to 10000: {removed_text(remove_stones(wide))}")
    sparse = random_stones(1000, 1000, 1000)
    print(f"1000 stones at random points up to 999: {removed_text(remove_stones(sparse))}")
    stairs = [[i // 2, (i + 1) // 2] for i in range(1000)]
    print(f"1000 stones in a staircase: {removed_text(remove_stones(stairs))}")
    diagonal = [[i * 10, 9990 - i * 10] for i in range(1000)]
    print(f"1000 stones on a diagonal: {removed_text(remove_stones(diagonal))}")
    grid = [[i // 40 * 400, i % 40 * 250] for i in range(1000)]
    print(f"25 rows of 40 stones: {removed_text(remove_stones(grid))}")


main()
