# LeetCode #2184: Number of Ways to Build Sturdy Brick Wall -- the
# benchmark's Python mirror of sturdy_wall.kara.

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


seed = 2184


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(1000):
        height = next_random() % 51 + 50
        bricks = [1]
        for b in range(2, 11):
            if next_random() % 2 == 0:
                bricks.append(b)
        check = (check * 31 + build_wall(height, 10, bricks)) % 1000000007
    print(f"1000 walls: checksum {check}")


main()
