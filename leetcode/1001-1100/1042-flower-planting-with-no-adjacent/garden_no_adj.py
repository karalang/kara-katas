# LeetCode #1042: Flower Planting With No Adjacent -- Python mirror of
# garden_no_adj.kara (greedy over the gardens in order), same harness.


def garden_no_adj(n, paths):
    neighbors = [[] for _ in range(n)]
    for x, y in paths:
        neighbors[x - 1].append(y - 1)
        neighbors[y - 1].append(x - 1)
    answer = [0] * n
    for garden in range(n):
        taken = [False] * 5
        for other in neighbors[garden]:
            taken[answer[other]] = True
        flower = 1
        while taken[flower]:
            flower += 1
        answer[garden] = flower
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(answer):
    return "[" + ", ".join(str(f) for f in answer) + "]"


def fold_into(check, answer):
    for flower in answer:
        check = (check * 131 + flower) % 1000000007
    return check


def random_paths(n, tries, seed):
    joined = [[] for _ in range(n)]
    paths = []
    for _ in range(tries):
        x = next_random(seed) % n
        y = next_random(seed) % n
        if x != y and len(joined[x]) < 3 and len(joined[y]) < 3 and y not in joined[x]:
            joined[x].append(y)
            joined[y].append(x)
            paths.append((x + 1, y + 1))
    return paths


def main():
    examples = [
        (3, [(1, 2), (2, 3), (3, 1)]),
        (4, [(1, 2), (3, 4)]),
        (4, [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3), (2, 4)]),
        (1, []),
        (5, [(5, 1), (4, 1), (3, 1)]),
        (6, [(6, 5), (5, 4), (4, 3), (3, 2), (2, 1)]),
        (7, [(1, 2), (2, 3), (3, 1), (5, 6), (6, 7), (7, 5)]),
        (8, [(1, 2), (2, 3), (3, 4), (4, 1), (5, 6), (6, 7), (7, 8), (8, 5), (1, 5), (2, 6), (3, 7), (4, 8)]),
        (10, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 8), (8, 10), (10, 7), (7, 9), (9, 6)]),
        (5, [(1, 5), (2, 5), (3, 5), (1, 4), (2, 4), (3, 4)]),
    ]
    for n, paths in examples:
        print(f"n = {n}, {len(paths)} paths -> {show(garden_no_adj(n, paths))}")
    for n in range(1, 7):
        pairs = [(x, y) for x in range(1, n + 1) for y in range(x + 1, n + 1)]
        gardens = 0
        four = 0
        check = 0
        for mask in range(1 << len(pairs)):
            paths = []
            degree = [0] * (n + 1)
            for i, (x, y) in enumerate(pairs):
                if (mask >> i) & 1 == 1:
                    paths.append((x, y))
                    degree[x] += 1
                    degree[y] += 1
            if all(d <= 3 for d in degree):
                answer = garden_no_adj(n, paths)
                gardens += 1
                if 4 in answer:
                    four += 1
                check = fold_into(check, answer)
        print(f"{n} plots: {gardens} gardens, {four} need four types, checksum {check}")
    seed = [1042]
    total = 0
    four = 0
    check = 0
    for _ in range(300):
        n = next_random(seed) % 50 + 1
        tries = next_random(seed) % (2 * n + 1)
        paths = random_paths(n, tries, seed)
        total += len(paths)
        answer = garden_no_adj(n, paths)
        if 4 in answer:
            four += 1
        check = fold_into(check, answer)
    print(f"300 random gardens: {total} paths, {four} need four types, checksum {check}")
    paths = random_paths(10000, 40000, seed)
    answer = garden_no_adj(10000, paths)
    counts = [0] * 5
    for flower in answer:
        counts[flower] += 1
    check = fold_into(0, answer)
    print(f"10000 plots, {len(paths)} paths: types {counts[1]} {counts[2]} {counts[3]} {counts[4]}, checksum {check}")


main()
