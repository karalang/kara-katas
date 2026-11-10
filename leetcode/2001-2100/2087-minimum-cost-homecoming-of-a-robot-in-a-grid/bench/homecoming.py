# LeetCode #2087: Minimum Cost Homecoming of a Robot in a Grid -- Python
# mirror of the ★ arm's benchmark (homecoming.kara): the same grid and
# 2000 trips, each the two ranges of costs summed, from copied slices.

seed = 2087


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def walk(costs, a, b):
    return sum(costs[a + 1:b + 1]) if a < b else sum(costs[b:a])


def min_cost(start, home, rows, cols):
    return walk(rows, start[0], home[0]) + walk(cols, start[1], home[1])


def place():
    hi = next_random()
    return (hi * 32768 + next_random()) % 1000000


def main():
    rows = [next_random() % 10001 for _ in range(1000000)]
    cols = [next_random() % 10001 for _ in range(1000000)]
    total = check = 0
    for _ in range(2000):
        r = place()
        start = [r, place()]
        r = place()
        home = [r, place()]
        a = min_cost(start, home, rows, cols)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 trips: sum {total}, checksum {check}")


main()
