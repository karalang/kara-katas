# LeetCode 780 — Reaching Points, backwards by remainders.
# Mirrors reaching_points.kara (the ★ arm) and its harness.


def reaching_points(sx, sy, tx, ty):
    x, y = tx, ty
    while x > sx and y > sy and x != y:
        if x > y:
            x %= y
        else:
            y %= x
    if x == sx and y == sy:
        return True
    if x == sx and y > sy:
        return (y - sy) % x == 0
    if y == sy and x > sx:
        return (x - sx) % y == 0
    return False


seed = 780


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(sx, sy, tx, ty):
    print(f"({sx}, {sy}) -> ({tx}, {ty}): {str(reaching_points(sx, sy, tx, ty)).lower()}")


def walk(x, y, moves):
    for _ in range(moves):
        if next_random() % 2 == 0:
            x += y
        else:
            y += x
    return x, y


def main():
    show(1, 1, 3, 5)
    show(1, 1, 2, 2)
    show(1, 1, 1, 1)
    show(1, 1, 1000000000, 1)
    show(1, 1, 1000000000, 999999999)
    show(3, 7, 3, 4)
    show(9, 5, 12, 8)
    show(2, 4, 2, 1000000000)
    show(2, 4, 2, 999999999)
    show(35, 13, 960682455, 554650274)
    show(35, 13, 960682455, 554650273)
    yes = 0
    check = 0
    for case in range(400):
        sx = 1 + next_random() % 20
        sy = 1 + next_random() % 20
        if case % 2 == 0:
            tx, ty = walk(sx, sy, next_random() % 30)
        else:
            tx = sx + next_random() % 2000
            ty = sy + next_random() % 2000
        answer = reaching_points(sx, sy, tx, ty)
        if answer:
            yes += 1
        check = (check * 31 + (tx % 1000 if answer else ty % 1000) + 1) % 1000000007
    print(f"400 random pairs: {yes} reachable, checksum {check}")


main()
