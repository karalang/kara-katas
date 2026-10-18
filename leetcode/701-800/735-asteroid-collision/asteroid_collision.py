# LeetCode #735: Asteroid Collision -- mirror of the star arm.


def asteroid_collision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            top = stack[-1]
            if top < -a:
                stack.pop()
            else:
                if top == -a:
                    stack.pop()
                alive = False
        if alive:
            stack.append(a)
    return stack


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(row):
    print(f"{fmt(row)} -> {fmt(asteroid_collision(row))}")


def digest(what, row):
    left = asteroid_collision(row)
    total = 0
    for a in left:
        total = (total * 131 + a + 1001) % 1000000007
    print(f"{what} -> {len(left)} left, checksum {total}")


def main():
    global seed
    show([5, 10, -5])
    show([8, -8])
    show([10, 2, -5])
    show([-2, -1, 1, 2])
    show([1, -2, -2, -2])
    show([3, 2, 1, -6, 4])
    show([-1, 3, -3, 2, -1, -2])
    show([1, 2, 3, -3, -2, -1])
    seed = 735
    random = []
    for _ in range(10000):
        size = 1 + next_random() % 1000
        random.append(size if next_random() % 2 == 0 else -size)
    digest("10000 random asteroids", random)
    wall = [1 + i % 999 for i in range(9999)] + [-1000]
    digest("9999 right-movers and one large left-mover", wall)
    pairs = []
    for i in range(5000):
        pairs.append(1 + i % 1000)
        pairs.append(-(1 + i % 1000))
    digest("5000 equal pairs", pairs)
    nested = [1 + i % 1000 for i in range(5000)] + [-(1 + (4999 - i) % 1000) for i in range(5000)]
    digest("5000 right-movers met by their mirror", nested)
    total = 0
    left = 0
    for _ in range(300):
        n = 2 + next_random() % 12
        row = []
        for _ in range(n):
            size = 1 + next_random() % 5
            row.append(size if next_random() % 2 == 0 else -size)
        out = asteroid_collision(row)
        left += len(out)
        for a in out:
            total = (total * 131 + a + 1001) % 1000000007
        total = (total * 131 + 7) % 1000000007
    print(f"300 random rows: {left} left, checksum {total}")


main()
