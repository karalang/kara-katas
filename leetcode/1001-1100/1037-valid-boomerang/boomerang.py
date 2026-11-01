# LeetCode #1037: Valid Boomerang -- Python mirror of boomerang.kara


def is_boomerang(points):
    (ax, ay), (bx, by), (cx, cy) = points
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) != 0


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(b):
    return "true" if b else "false"


def main():
    examples = [
        [(1, 1), (2, 3), (3, 2)],
        [(1, 1), (2, 2), (3, 3)],
        [(0, 0), (0, 0), (1, 1)],
        [(0, 0), (1, 1), (0, 0)],
        [(5, 5), (5, 5), (5, 5)],
        [(0, 0), (0, 5), (0, 100)],
        [(0, 0), (100, 0), (0, 100)],
        [(0, 0), (99, 100), (100, 100)],
        [(0, 0), (49, 50), (98, 100)],
        [(0, 1), (50, 51), (100, 100)],
    ]
    for points in examples:
        a, b, c = points
        print(f"{a}, {b}, {c} -> {show(is_boomerang(points))}")
    for side in [3, 5]:
        yes = 0
        check = 0
        count = 0
        for p in range(side * side):
            for q in range(side * side):
                for r in range(side * side):
                    answer = is_boomerang([(p // side, p % side), (q // side, q % side), (r // side, r % side)])
                    if answer:
                        yes += 1
                    check = (check * 131 + (2 if answer else 1)) % 1000000007
                    count += 1
        print(f"all {count} triples on a {side} by {side} grid: {yes} boomerangs, checksum {check}")
    seed = [1037]
    yes = 0
    check = 0
    for k in range(3000):
        a = (next_random(seed) % 101, next_random(seed) % 101)
        b = (next_random(seed) % 101, next_random(seed) % 101)
        if k % 3 == 0:
            c = (next_random(seed) % 101, next_random(seed) % 101)
        else:
            ax, ay = a
            bx, by = b
            t = next_random(seed) % 3 - 1
            off = 0 if k % 3 == 1 else 1
            c = (ax + t * (bx - ax) + off, ay + t * (by - ay))
        answer = is_boomerang([a, b, c])
        if answer:
            yes += 1
        check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"3000 random triples: {yes} boomerangs, checksum {check}")


main()
