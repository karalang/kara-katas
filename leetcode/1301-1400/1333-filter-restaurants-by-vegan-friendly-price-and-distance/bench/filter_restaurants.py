# LeetCode #1333 bench, Python mirror of the Kāra bench: the ★ arm on 20
# lists of 10^4 restaurants built once, then 100 passes, each setting one
# rating of every list from the checksum so far and drawing the filters
# from it too, answering every list.


def filter_restaurants(restaurants, vegan_friendly, max_price, max_distance):
    kept = [(r[1], r[0]) for r in restaurants
            if (vegan_friendly == 0 or r[2] == 1) and r[3] <= max_price and r[4] <= max_distance]
    kept.sort(key=lambda p: (-p[0], -p[1]))
    return [p[1] for p in kept]


seed = 1333


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 10000
    lists = []
    for _ in range(20):
        lst = []
        for i in range(n):
            id_ = i * 10 + 1 + next_random() % 10
            rating = 1 + next_random() % 100000
            vegan = next_random() % 2
            price = 1 + next_random() % 100000
            distance = 1 + next_random() % 100000
            lst.append([id_, rating, vegan, price, distance])
        lists.append(lst)
    check = 0
    for p in range(100):
        vegan = p % 2
        max_price = 50000 + check % 50001
        max_distance = 50000 + check // 7 % 50001
        for t in range(20):
            at = check % n
            lists[t][at][1] = 1 + check // 3 % 100000
            ids = filter_restaurants(lists[t], vegan, max_price, max_distance)
            k = len(ids)
            check = (check * 31 + k + ids[0] + ids[k // 2] + p) % 1000000007
    print(f"100 passes over 20 lists of 10^4: checksum {check}")


main()
