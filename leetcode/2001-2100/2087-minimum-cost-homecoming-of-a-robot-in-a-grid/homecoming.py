# LeetCode #2087: Minimum Cost Homecoming of a Robot in a Grid -- Python
# mirror of the ★ arm (homecoming.kara): the rows' and the columns' costs
# between start and home, two ranges summed.

seed = 2087


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def walk(costs, a, b):
    return sum(costs[a + 1:b + 1]) if a < b else sum(costs[b:a])


def min_cost(start, home, rows, cols):
    return walk(rows, start[0], home[0]) + walk(cols, start[1], home[1])


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([1, 0], [2, 3], [5, 4, 3], [8, 2, 6, 7]),
        ([0, 0], [0, 0], [5], [26]),
        ([2, 3], [1, 0], [5, 4, 3], [8, 2, 6, 7]),
        ([0, 2], [3, 2], [1, 2, 3, 4], [9, 9, 9]),
        ([1, 1], [1, 0], [7, 7], [0, 5]),
        ([4, 0], [0, 4], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([0, 0], [2, 2], [0, 0, 0], [0, 0, 0]),
    ]
    for s, h, r, c in examples:
        print(f"{show(s)} {show(h)} {show(r)} {show(c)} -> {min_cost(s, h, r, c)}")
    total = check = 0
    for _ in range(2000):
        m = next_random() % 50 + 1
        n = next_random() % 50 + 1
        rows = [next_random() % 10001 for _ in range(m)]
        cols = [next_random() % 10001 for _ in range(n)]
        start = [next_random() % m]
        start.append(next_random() % n)
        home = [next_random() % m]
        home.append(next_random() % n)
        a = min_cost(start, home, rows, cols)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 grids: sum {total}, checksum {check}")
    rows = [next_random() % 10001 for _ in range(100000)]
    cols = [next_random() % 10001 for _ in range(100000)]
    print(f"10^5 by 10^5, corner to corner: {min_cost([0, 0], [99999, 99999], rows, cols)}")
    print(f"10^5 by 10^5, back: {min_cost([99999, 99999], [0, 0], rows, cols)}")


main()
