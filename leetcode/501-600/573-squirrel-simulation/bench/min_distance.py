# Benchmark for #573: Python mirror of the ★ arm (one pass with the best
# first nut); see min_distance.kara.


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def min_distance(height, width, tree, squirrel, nuts):
    total = 0
    best_saving = -(2**63)
    for nut in nuts:
        to_tree = distance(nut, tree)
        total += 2 * to_tree
        best_saving = max(best_saving, to_tree - distance(nut, squirrel))
    return total - best_saving


# ---- benchmark --------------------------------------------------------------

seed = 573


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def cell():
    r = next_random() % 100
    return [r, next_random() % 100]


def main():
    count = 20
    rounds = 2000
    trees = []
    squirrels = []
    nut_sets = []
    for _ in range(count):
        trees.append(cell())
        squirrels.append(cell())
        nut_sets.append([cell() for _ in range(5000)])
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            p = (rnd * 7 + g) % count
            got = min_distance(100, 100, trees[p], squirrels[p], nut_sets[p])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} cases of 5000 nuts, {rounds} rounds: {total} steps, checksum {checksum}")


main()
