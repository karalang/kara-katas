# Benchmark for #554: Python mirror of the ★ arm (count the edges at
# each position); see brick_wall.kara.

seed = 554


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    count = 20
    walls = []
    bricks = 0
    for _ in range(count):
        wall = []
        n = 0
        while n < 19000:
            row = []
            left = 1000000
            while left > 0:
                a = next_random()
                b = next_random()
                w = 1 + (a * 32768 + b) % 10000
                w = min(w, left)
                row.append(w)
                left -= w
            n += len(row)
            wall.append(row)
        bricks += n
        walls.append(wall)
    total = 0
    checksum = 0
    for rnd in range(50):
        for g in range(count):
            got = least_bricks(walls[(rnd * 7 + g) % count])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} walls, {bricks} bricks, 50 rounds each: total {total}, checksum {checksum}")


main()
