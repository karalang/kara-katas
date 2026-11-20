# LeetCode #1232 bench: the ★ arm in Python, over the same 1000 sets of
# 1000 points and 200 passes as the Kāra bench.


def check_straight_line(coordinates):
    dx = coordinates[1][0] - coordinates[0][0]
    dy = coordinates[1][1] - coordinates[0][1]
    for p in coordinates:
        if (p[0] - coordinates[0][0]) * dy != (p[1] - coordinates[0][1]) * dx:
            return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1232]
    sets = []
    for s in range(1000):
        dx = next_random(seed) % 21 - 10
        dy = next_random(seed) % 21 - 10
        if dx == 0 and dy == 0:
            dx = 1
        pts = [[t * dx, t * dy] for t in range(1000)]
        if s % 2 == 1:
            if dx == 0:
                pts[999][0] += 1
            else:
                pts[999][1] += 1
        sets.append(pts)
    straight = 0
    for _ in range(200):
        for pts in sets:
            if check_straight_line(pts):
                straight += 1
    print(f"1000 sets of 1000 points, 200 passes: {straight} straight")


main()
