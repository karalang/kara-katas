# LeetCode #573: Squirrel Simulation -- Python mirror of the ★ arm (one
# pass with the best first nut); see min_distance.kara.


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


# ---- test harness ---------------------------------------------------------

seed = 573


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, height, width, tree, squirrel, nuts):
    print(f"{name}: {min_distance(height, width, tree, squirrel, nuts)}")


def random_cell(height, width):
    r = next_random() % height
    return [r, next_random() % width]


def main():
    show("example 1", 5, 7, [2, 2], [4, 4], [[3, 0], [2, 5]])
    show("example 2", 1, 3, [0, 1], [0, 0], [[0, 2]])
    show("squirrel on a nut", 3, 3, [0, 0], [2, 2], [[2, 2], [0, 2]])
    show("squirrel at the tree", 3, 3, [1, 1], [1, 1], [[0, 0], [2, 2]])
    show("a nut at the tree", 3, 3, [1, 1], [0, 0], [[1, 1], [2, 2]])
    show("not the nearest", 1, 10, [0, 4], [0, 2], [[0, 3], [0, 0]])
    show("all alike", 1, 10, [0, 5], [0, 0], [[0, 7], [0, 9]])
    show("one cell", 1, 1, [0, 0], [0, 0], [[0, 0]])
    total = 0
    checksum = 0
    for _ in range(300):
        height = 1 + next_random() % 10
        width = 1 + next_random() % 10
        tree = random_cell(height, width)
        squirrel = random_cell(height, width)
        nuts = []
        for _ in range(1 + next_random() % 8):
            nuts.append(random_cell(height, width))
        got = min_distance(height, width, tree, squirrel, nuts)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random cases: {total} steps, checksum {checksum}")
    tree = random_cell(100, 100)
    squirrel = random_cell(100, 100)
    nuts = [random_cell(100, 100) for _ in range(5000)]
    print(f"100 by 100, 5000 nuts at random: {min_distance(100, 100, tree, squirrel, nuts)}")
    corner = [[99 - i % 10, 99 - i // 10 % 10] for i in range(5000)]
    show("100 by 100, 5000 nuts in a corner", 100, 100, [0, 0], [0, 99], corner)


main()
