# Benchmark for #780: Reaching Points -- mirror of the ★ arm (backwards
# by remainders), with the same workload as the Kāra program.


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


def main():
    count = 1024
    queries = []
    for q in range(count):
        sx = 1 + next_random() % 1000
        sy = 1 + next_random() % 1000
        a = sx + 1 if q % 4 == 3 else sx
        b = sy
        while a <= 500000000 and b <= 500000000:
            if next_random() % 2 == 0:
                a += b
            else:
                b += a
        if q % 4 == 2:
            b -= 1
        queries.append((sx, sy, a, b))
    yes = 0
    checksum = 0
    for rnd in range(15000):
        for i in range(count):
            sx, sy, tx, ty = queries[i]
            if reaching_points(sx, sy, tx, ty):
                yes += 1
                checksum = (checksum * 31 + i + rnd) % 1000000007
    print(f"15000 rounds of 1024 queries: {yes} reachable, checksum {checksum}")


main()
