# LeetCode #1042: Flower Planting With No Adjacent -- bench, Python
# mirror of garden_no_adj.kara (greedy over the gardens in order).


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
    count = 10
    n = 10000
    rounds = 100
    seed = [1042]
    gardens = [random_paths(n, 4 * n, seed) for _ in range(count)]
    total = 0
    check = 0
    for _ in range(rounds):
        for paths in gardens:
            answer = garden_no_adj(n, paths)
            s = sum(answer)
            total += s
            check = (check * 131 + s) % 1000000007
    print(f"{count} gardens of {n} plots, {rounds} rounds: types sum to {total}, checksum {check}")


main()
