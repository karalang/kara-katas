# Benchmark for #547: Python mirror of the ★ arm (depth-first search);
# see number_of_provinces.kara.
import sys

sys.setrecursionlimit(10000)


def visit(m, city, seen):
    seen[city] = True
    row = m[city]
    for other in range(len(m)):
        if row[other] == 1 and not seen[other]:
            visit(m, other, seen)


def find_circle_num(m):
    n = len(m)
    seen = [False] * n
    provinces = 0
    for city in range(n):
        if not seen[city]:
            provinces += 1
            visit(m, city, seen)
    return provinces


seed = 547


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, n = 30, 200
    all_m = []
    for g in range(count):
        m = [[0] * n for _ in range(n)]
        for i in range(n):
            m[i][i] = 1
        for i in range(n):
            for j in range(i + 1, n):
                if next_random() % 1000 < 1 + g % 10:
                    m[i][j] = 1
                    m[j][i] = 1
        all_m.append(m)
    total = checksum = 0
    for rnd in range(200):
        for g in range(count):
            a, b = (rnd * 13 + g) % n, (rnd * 29 + g * 3 + 1) % n
            if a != b:
                flip = 1 - all_m[g][a][b]
                all_m[g][a][b] = flip
                all_m[g][b][a] = flip
            p = find_circle_num(all_m[g])
            total += p
            checksum = (checksum * 31 + p) % 1000000007
    print(f"{count} matrices, 200 rounds each: {total} provinces, checksum {checksum}")


main()
