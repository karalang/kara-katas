# LeetCode #547: Number of Provinces -- Python mirror of the ★ arm
# (depth-first search); see number_of_provinces.kara.
import sys

sys.setrecursionlimit(10000)


def visit(is_connected, city, seen):
    seen[city] = True
    for other in range(len(is_connected)):
        if is_connected[city][other] == 1 and not seen[other]:
            visit(is_connected, other, seen)


def find_circle_num(is_connected):
    n = len(is_connected)
    seen = [False] * n
    provinces = 0
    for city in range(n):
        if not seen[city]:
            provinces += 1
            visit(is_connected, city, seen)
    return provinces


# ---- test harness ---------------------------------------------------------

seed = 547


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def alone(n):
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = 1
    return m


def join(m, a, b):
    m[a][b] = 1
    m[b][a] = 1


def random_matrix(n, chance):
    m = alone(n)
    for i in range(n):
        for j in range(i + 1, n):
            if next_random() % 1000 < chance:
                join(m, i, j)
    return m


def show(name, m):
    print(f"{name}: {find_circle_num(m)}")


def main():
    show("example 1", [[1, 1, 0], [1, 1, 0], [0, 0, 1]])
    show("example 2", [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    show("one city", [[1]])
    show("two cities joined", [[1, 1], [1, 1]])
    show("a chain of four", [[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]])
    show("the first and last of five joined", [[1, 0, 0, 0, 1], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [1, 0, 0, 0, 1]])
    cities = total = h = 0
    for t in range(300):
        n = 1 + next_random() % 40
        chance = 2 if t % 3 == 0 else 20 if t % 3 == 1 else 80
        p = find_circle_num(random_matrix(n, chance))
        cities += n
        total += p
        h = (h * 31 + p) % 1000000007
    print(f"300 random matrices: {cities} cities, {total} provinces, checksum {h}")
    show("200 cities alone", alone(200))
    show("200 cities all joined", [[1] * 200 for _ in range(200)])
    chain = alone(200)
    for i in range(199):
        join(chain, i, i + 1)
    show("200 cities in a chain", chain)
    hub = alone(200)
    for i in range(100):
        join(hub, 199, 2 * i)
    show("a hub joined to the even cities", hub)
    show("200 random cities, chance 5 in 1000", random_matrix(200, 5))


main()
