# LeetCode #735: Asteroid Collision -- a stack of survivors.
# Benchmark mirror of the Kara star arm: walk the row keeping the
# survivors so far on a stack; a left-mover destroys the smaller
# right-movers on top, then is destroyed by a larger one, dies with an
# equal one, or survives onto the stack.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [735]
    rows = []
    for _ in range(20):
        row = []
        for _ in range(10000):
            size = 1 + next_random(seed) % 1000
            row.append(size if next_random(seed) % 2 == 0 else -size)
        rows.append(row)
    left = 0
    total = 0
    for _ in range(500):
        for k in range(20):
            j = next_random(seed) % 10000
            rows[k][j] = -rows[k][j]
            survivors = asteroid_collision(rows[k])
            left += len(survivors)
            for a in survivors:
                total = (total * 31 + a + 1000) % 1000000007
    print(f"500 rounds of 20 rows of 10000 asteroids: {left} left, checksum {total}")


main()
