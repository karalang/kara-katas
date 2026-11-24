# LeetCode #1333: Filter Restaurants by Vegan-Friendly, Price and Distance
# -- Python mirror of the ★ arm: the restaurants that pass, sorted by
# rating and then id, both highest first.


def filter_restaurants(restaurants, vegan_friendly, max_price, max_distance):
    kept = [(r[1], r[0]) for r in restaurants
            if (vegan_friendly == 0 or r[2] == 1) and r[3] <= max_price and r[4] <= max_distance]
    kept.sort(key=lambda p: (-p[0], -p[1]))
    return [p[1] for p in kept]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, ids):
    c = check
    for i in ids:
        c = (c * 131 + i) % 1000000007
    return (c * 131 + 7) % 1000000007


def draw(n, spread, ratings, limit):
    ids = [i * spread + 1 + next_random() % spread for i in range(n)]
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        ids[i], ids[j] = ids[j], ids[i]
    out = []
    for i in range(n):
        rating = 1 + next_random() % ratings
        vegan = next_random() % 2
        price = 1 + next_random() % limit
        distance = 1 + next_random() % limit
        out.append([ids[i], rating, vegan, price, distance])
    return out


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    ex = [[1, 4, 1, 40, 10], [2, 8, 0, 50, 5], [3, 8, 1, 30, 4], [4, 10, 0, 10, 3], [5, 1, 1, 15, 1]]
    print(f"{show(filter_restaurants(ex, 1, 50, 10))} {show(filter_restaurants(ex, 0, 50, 10))} {show(filter_restaurants(ex, 0, 30, 3))}")
    print(f"{show(filter_restaurants(ex, 1, 5, 5))} {show(filter_restaurants([[7, 3, 0, 20, 9]], 0, 20, 9))}")
    seed = 1333
    big = draw(10000, 10, 50, 100000)
    al = filter_restaurants(big, 0, 100000, 100000)
    some = filter_restaurants(big, 1, 60000, 70000)
    print(f"10^4 restaurants: {len(al)} first {al[0]}, {len(some)} vegan first {some[0]}, checksum {fold(fold(0, al), some)}")
    check = 0
    kept = 0
    for t in range(600):
        n = 1 + next_random() % 2000 if t % 20 == 0 else 1 + next_random() % 12
        ratings = 3 if t % 2 == 0 else 100000
        limit = 100000 if t % 3 == 0 else 10
        lst = draw(n, 1 + t % 5, ratings, limit)
        vegan = next_random() % 2
        max_price = 1 + next_random() % limit
        max_distance = 1 + next_random() % limit
        ids = filter_restaurants(lst, vegan, max_price, max_distance)
        kept += len(ids)
        check = fold(check, ids)
    print(f"600 random lists: {kept} kept, checksum {check}")


main()
