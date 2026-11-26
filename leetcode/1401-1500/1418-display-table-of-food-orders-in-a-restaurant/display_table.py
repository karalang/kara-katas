# LeetCode #1418, Python mirror of display_table.kara: each table's count
# of each dish, the tables in order, and the dishes anyone ordered, in
# order, for the header.


def display_table(orders):
    tables = {}
    foods = set()
    for order in orders:
        table = int(order[1])
        foods.add(order[2])
        counts = tables.setdefault(table, {})
        counts[order[2]] = counts.get(order[2], 0) + 1
    header = ["Table"] + sorted(foods)
    out = [header]
    for table in sorted(tables):
        counts = tables[table]
        out.append([str(table)] + [str(counts.get(food, 0)) for food in sorted(foods)])
    return out


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def parsed(text):
    return [order.split(",") for order in text.split(";")]


LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def dish():
    n = 1 + next_random() % 20
    s = []
    for _ in range(n):
        r = next_random()
        s.append(" " if r % 6 == 0 else LETTERS[r // 6 % 52])
    return "".join(s)


def drawn(n, tables, dishes):
    pool = [dish() for _ in range(dishes)]
    names = ["David", "Corina", "Carla", "Rous", "James"]
    orders = []
    for _ in range(n):
        r = next_random()
        food = pool[next_random() % dishes]
        orders.append([names[r % 5], str(1 + r // 5 % tables), food])
    return orders


def shown(table):
    return "|".join(",".join(row) for row in table)


def checksum(check, text):
    for b in text.encode():
        check = (check * 131 + b) % 1000000007
    return (check * 131 + 7) % 1000000007


def main():
    global seed
    examples = [
        "David,3,Ceviche;Corina,10,Beef Burrito;David,3,Fried Chicken;Carla,5,Water;Carla,5,Ceviche;Rous,3,Ceviche",
        "James,12,Fried Chicken;Ratesh,12,Fried Chicken;Amadeus,12,Fried Chicken;Adam,1,Canadian Waffles;Brianna,1,Canadian Waffles",
        "Laura,2,Bean Burrito;Jhon,2,Beef Burrito;Melissa,2,Soda",
        "Ann,500,ab;Bo,1,a b;Ann,500,Ab;Cy,1,ab;Bo,1,ab",
    ]
    for text in examples:
        print(shown(display_table(parsed(text))))
    seed = 1418
    big = display_table(drawn(50000, 500, 20))
    print(f"5 * 10^4 orders: {len(big)} rows of {len(big[0])} cells, checksum {checksum(0, shown(big))}")
    check = 0
    rows = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        tables = 5 if next_random() % 2 == 0 else 500
        dishes = 1 + next_random() % 8
        table = display_table(drawn(n, tables, dishes))
        rows += len(table)
        check = checksum(check, shown(table))
    print(f"2000 random cases: {rows} rows, checksum {check}")


main()
