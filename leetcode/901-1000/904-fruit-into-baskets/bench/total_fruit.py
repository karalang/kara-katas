# LeetCode #904: Fruit Into Baskets -- bench program, Python.
#
# The last two types and the last run, over one row of 1,000,000 trees
# built once, of 3 types in runs of 1 to 50 trees. Each round finds the
# most fruit, folds it into a checksum and changes one tree's type.


def total_fruit(fruits):
    last = -1
    before = -1
    run = 0
    current = 0
    best = 0
    for f in fruits:
        if f == last or f == before:
            current += 1
        else:
            current = run + 1
        if f == last:
            run += 1
        else:
            run = 1
            before = last
            last = f
        best = max(best, current)
    return best


seed = 904


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    trees = 1000000
    rounds = 240
    fruits = []
    while len(fruits) < trees:
        f = next_random() % 3
        r = 1 + next_random() % 50
        for _ in range(r):
            if len(fruits) < trees:
                fruits.append(f)
    check = 0
    total = 0
    for r in range(rounds):
        got = total_fruit(fruits)
        total += got
        check = (check * 31 + got) % 1000000007
        fruits[r * 7919 % trees] = next_random() % 3
    print(f"{rounds} rounds over {trees} trees: answers summing to {total}, checksum {check}")


main()
