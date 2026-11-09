# LeetCode #2033: Minimum Operations to Make a Uni-Value Grid -- the ★ arm
# in Python, the same algorithm and workload as grid.kara.


def min_operations(grid, x):
    values = [v for row in grid for v in row]
    r = values[0] % x
    if any(v % x != r for v in values):
        return -1
    values.sort()
    median = values[len(values) // 2]
    return sum(abs(v - median) // x for v in values)


seed = 2033


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grids = []
    for a in range(20):
        x = a % 7 + 1
        base = next_random() % x + 1
        steps = (10000 - base) // x + 1
        grid = []
        for _ in range(200):
            row = []
            for _ in range(250):
                hi = next_random()
                lo = next_random()
                row.append(base + (hi * 32768 + lo) % steps * x)
            grid.append(row)
        grids.append(grid)
    calls = total = check = 0
    for rnd in range(30):
        for a in range(20):
            x = a % 7 + 1
            at = (rnd * 997 + a * 31) % 50000
            v = grids[a][at // 250][at % 250]
            grids[a][at // 250][at % 250] = v + x if v + x <= 10000 else v - x
            answer = min_operations(grids[a], x)
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
