# LeetCode #1418: the bench in Python, mirroring display_table.kara: each
# table's counts in a dict, the tables and the dishes then sorted.


def display_table(orders, lo, hi):
    tables = {}
    foods = set()
    for i in range(lo, hi):
        order = orders[i]
        table = int(order[1])
        foods.add(order[2])
        counts = tables.setdefault(table, {})
        counts[order[2]] = counts.get(order[2], 0) + 1
    names = sorted(foods)
    out = [["Table"] + names]
    for table in sorted(tables):
        counts = tables[table]
        out.append([str(table)] + [str(counts.get(f, 0)) for f in names])
    return out


seed = 1418


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dishes = []
    for _ in range(30):
        n = 1 + next_random() % 20
        s = []
        for _ in range(n):
            r = next_random()
            s.append(" " if r % 6 == 0 else letters[r // 6 % 52])
        dishes.append("".join(s))
    pool = []
    for _ in range(200000):
        r = next_random()
        food = dishes[next_random() % 30]
        pool.append([f"guest{r % 100}", str(1 + r // 100 % 500), food])
    check = 0
    for _ in range(100):
        start = next_random() % 150001
        for row in display_table(pool, start, start + 50000):
            for cell in row:
                for b in cell.encode():
                    check = (check * 131 + b) % 1000000007
                check = (check * 131 + 7) % 1000000007
    print(f"100 windows of 5 * 10^4 orders: checksum {check}")


main()
