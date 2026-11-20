# LeetCode #1232: Check If It Is a Straight Line -- Python mirror of the ★
# arm: every point's offset from the first parallel to the first two's, a
# cross product of zero.


def check_straight_line(coordinates):
    dx = coordinates[1][0] - coordinates[0][0]
    dy = coordinates[1][1] - coordinates[0][1]
    for p in coordinates:
        if (p[0] - coordinates[0][0]) * dy != (p[1] - coordinates[0][1]) * dx:
            return False
    return True


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def points(n, spread, bent, seed):
    x0 = next_random(seed) % (2 * spread + 1) - spread
    y0 = next_random(seed) % (2 * spread + 1) - spread
    dx = next_random(seed) % 21 - 10
    dy = next_random(seed) % 21 - 10
    if dx == 0 and dy == 0:
        dx = 1
    pts = [[x0 + t * dx, y0 + t * dy] for t in range(n)]
    for k in range(n):
        j = k + next_random(seed) % (n - k)
        pts[k], pts[j] = pts[j], pts[k]
    if bent:
        i = next_random(seed) % n
        if dx == 0:
            pts[i][0] += 1
        else:
            pts[i][1] += 1
    return pts


def show(b):
    return "true" if b else "false"


def main():
    # LeetCode's two examples, two points, an upright and a level line
    print(show(check_straight_line([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])))
    print(show(check_straight_line([[1, 1], [2, 2], [3, 4], [4, 5], [5, 6], [7, 7]])))
    print(show(check_straight_line([[0, 0], [5, -3]])))
    print(show(check_straight_line([[2, -1], [2, 7], [2, 3], [2, 0]])))
    print(show(check_straight_line([[-4, 9], [8, 9], [0, 9], [0, 8]])))
    # 1000 random sets of 2 to 40 points, half of them with one moved
    seed = [1232]
    straight = 0
    check = 0
    for c in range(1000):
        n = next_random(seed) % 39 + 2
        pts = points(n, 100, c % 2 == 1, seed)
        on = check_straight_line(pts)
        if on:
            straight += 1
        check = (check * 131 + (2 if on else 1)) % 1000000007
    print(f"1000 random sets: {straight} straight, checksum {check}")
    # the constraints' top: 1000 points within 10^4, straight and one moved
    line = points(1000, 0, False, seed)
    bent = points(1000, 0, True, seed)
    print(f"1000 points: {show(check_straight_line(line))}, {show(check_straight_line(bent))}")


main()
