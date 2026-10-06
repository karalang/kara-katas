# Benchmark for #356 -- same workload and algorithm as line_reflection.kara.


def is_reflected(points):
    if not points:
        return True
    lo = points[0][0]
    hi = points[0][0]
    seen = set()
    for x, y in points:
        lo = min(lo, x)
        hi = max(hi, x)
        seen.add((x, y))
    s = lo + hi
    for x, y in points:
        if (s - x, y) not in seen:
            return False
    return True


def main():
    seed = 356
    yes = 0
    checksum = 0
    for rnd in range(400):
        seed = (seed * 1103515245 + 12345) % 2147483648
        center2 = (seed // 16) % 2000001 - 1000000
        points = []
        for _ in range(2500):
            seed = (seed * 1103515245 + 12345) % 2147483648
            x = (seed // 16) % 2000001 - 1000000
            seed = (seed * 1103515245 + 12345) % 2147483648
            y = (seed // 65536) % 1000
            points.append((x, y))
            points.append((center2 - x, y))
        if rnd % 3 == 0:
            seed = (seed * 1103515245 + 12345) % 2147483648
            i = (seed // 65536) % len(points)
            points[i] = (points[i][0] + 1, points[i][1])
        r = is_reflected(points)
        if r:
            yes += 1
        checksum = (checksum * 3 + (1 if r else 2)) % 1000000007
    print(f"{yes} of 400 sets reflect, checksum {checksum}")


main()
