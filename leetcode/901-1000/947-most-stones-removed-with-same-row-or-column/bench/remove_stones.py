# Benchmark: LeetCode #947 Most Stones Removed with Same Row or Column --
# the ★ arm, rows and columns joined, on sets of 1000 stones, LeetCode's
# largest. Mirrors remove_stones.kara, .c, .rs and go-seq/.


def find_line(parent, v):
    x = v
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def remove_stones(stones):
    parent = [-1] * 20002
    groups = 0
    for s in stones:
        row = s[0]
        col = 10001 + s[1]
        if parent[row] < 0:
            parent[row] = row
            groups += 1
        if parent[col] < 0:
            parent[col] = col
            groups += 1
        a = find_line(parent, row)
        b = find_line(parent, col)
        if a != b:
            parent[a] = b
            groups -= 1
    return len(stones) - groups


seed = 947


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 1000, 20, 1000
    sets = []
    for _ in range(count):
        side = 200 + next_random() % 1801
        taken = set()
        stones = []
        while len(stones) < n:
            x = next_random() % side
            y = next_random() % side
            if x * 10001 + y not in taken:
                taken.add(x * 10001 + y)
                stones.append([x, y])
        sets.append(stones)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            m = remove_stones(sets[(r + i) % count])
            total += m
            check = (check * 1000003 + m) % 1000000007
    print(f"{rounds} rounds over {count} sets of {n} stones: {total} removed, checksum {check}")


main()
