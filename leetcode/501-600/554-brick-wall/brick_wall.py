# LeetCode #554: Brick Wall -- Python mirror of the ★ arm (count the
# edges at each position); see brick_wall.kara.


def least_bricks(wall):
    edges = {}
    most = 0
    for row in wall:
        at = 0
        for j in range(len(row) - 1):
            at += row[j]
            count = edges.get(at, 0) + 1
            edges[at] = count
            if count > most:
                most = count
    return len(wall) - most


# ---- test harness ---------------------------------------------------------

seed = 554


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(wall):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in wall) + "]"


def show(wall):
    print(f"{fmt(wall)} -> {least_bricks(wall)}")


def random_row(width, widest):
    row = []
    left = width
    while left > 0:
        w = 1 + next_random() % widest
        w = min(w, left)
        row.append(w)
        left -= w
    return row


def main():
    show([[1, 2, 2, 1], [3, 1, 2], [1, 3, 2], [2, 4], [3, 1, 2], [1, 3, 1, 1]])
    show([[1], [1], [1]])
    show([[5]])
    show([[1, 1], [1, 1]])
    show([[2147483647], [2147483646, 1]])
    show([[1000000000, 1000000000], [2000000000], [1, 1999999999]])
    show([[1, 1, 1, 1], [2, 2], [4], [3, 1], [1, 3]])
    bricks = total = h = 0
    for _ in range(300):
        rows = 1 + next_random() % 20
        width = 1 + next_random() % 30
        wall = []
        for _ in range(rows):
            row = random_row(width, 5)
            bricks += len(row)
            wall.append(row)
        got = least_bricks(wall)
        total += got
        h = (h * 31 + got) % 1000000007
    print(f"300 random walls: {bricks} bricks, total {total}, checksum {h}")
    wall = []
    count = 0
    while count < 20000 - 300:
        row = random_row(300, 3)
        count += len(row)
        wall.append(row)
    print(f"{len(wall)} rows of 300, {count} bricks -> {least_bricks(wall)}")
    tall = [[2147483647] for _ in range(10000)]
    print(f"10000 rows of one brick -> {least_bricks(tall)}")


main()
