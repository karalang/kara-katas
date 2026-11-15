# LeetCode #2184: Number of Ways to Build Sturdy Brick Wall -- the Python
# mirror of sturdy_wall.kara: every way to fill a row, as the mask of
# its joints, the rows each can sit on listed once, and the rows stacked
# by a count over the last row.

MOD = 1000000007


def build_wall(height, width, bricks):
    rows = []

    def fill(at, joints):
        if at == width:
            rows.append(joints)
            return
        for b in bricks:
            if at + b <= width:
                fill(at + b, joints | (1 << (at + b)) if at + b < width else joints)

    fill(0, 0)
    fits = [[b for b in range(len(rows)) if rows[a] & rows[b] == 0] for a in range(len(rows))]
    ways = [1] * len(rows)
    for _ in range(height - 1):
        nxt = [0] * len(rows)
        for a in range(len(rows)):
            for b in fits[a]:
                nxt[b] = (nxt[b] + ways[a]) % MOD
        ways = nxt
    return sum(ways) % MOD


# ---- test harness ---------------------------------------------------------

seed = 2184


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(height, width, bricks):
    print(f"{height}, {width}, [{', '.join(map(str, bricks))}] -> {build_wall(height, width, bricks)}")


def main():
    show(2, 3, [1, 2])
    show(1, 1, [5])
    show(1, 4, [1, 2, 3, 4])
    show(3, 1, [1])
    show(2, 2, [1])
    show(100, 10, [1, 2, 3])
    total = 0
    check = 0
    for _ in range(300):
        height = next_random() % 10 + 1
        width = next_random() % 10 + 1
        bricks = []
        for b in range(1, 11):
            if next_random() % 3 == 0:
                bricks.append(b)
        if not bricks:
            bricks.append(next_random() % 10 + 1)
        found = build_wall(height, width, bricks)
        total = (total + found) % MOD
        check = (check * 31 + found + height * width) % MOD
    print(f"300 walls: {total} in all mod 10^9 + 7, checksum {check}")
    for bricks in [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2], [2, 3, 5]]:
        print(f"100 x 10 of {', '.join(map(str, bricks))}: {build_wall(100, 10, bricks)}")


main()
