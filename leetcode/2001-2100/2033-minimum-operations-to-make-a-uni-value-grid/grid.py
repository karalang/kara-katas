# LeetCode #2033: Minimum Operations to Make a Uni-Value Grid -- a Python
# mirror of the ★ arm (grid.kara): every value must leave the same remainder
# mod x; then the cost is the sum of |v - median| / x over the sorted values.


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


def mix(check, answer):
    return (check * 31 + answer + 2) % 1000000007


def random_grid(m, n, x, cap, aligned):
    base = next_random() % min(x, cap) + 1
    steps = (cap - base) // x + 1
    grid = []
    for _ in range(m):
        row = []
        for _ in range(n):
            if aligned:
                row.append(base + next_random() % steps * x)
            else:
                row.append(next_random() % cap + 1)
        grid.append(row)
    return grid


def main():
    examples = [
        ([[2, 4], [6, 8]], 2),
        ([[1, 5], [2, 3]], 1),
        ([[1, 2], [3, 4]], 2),
        ([[7]], 3),
        ([[1, 1], [1, 1]], 5),
        ([[1, 10000]], 9999),
        ([[1, 10000]], 3),
        ([[3, 6, 9, 12, 15]], 3),
        ([[5], [5], [5], [8]], 3),
        ([[2, 2, 2], [4, 4, 4]], 2),
    ]
    for grid, x in examples:
        print(f"{grid}, {x} -> {min_operations(grid, x)}")
    answered = total = check = 0
    for _ in range(3000):
        m = next_random() % 6 + 1
        n = next_random() % 6 + 1
        x = next_random() % 5 + 1
        cap = next_random() % 30 + 1
        aligned = next_random() % 4 != 0
        answer = min_operations(random_grid(m, n, x, cap, aligned), x)
        if answer >= 0:
            answered += 1
            total += answer
        check = mix(check, answer)
    print(f"3000 small grids: {answered} answered, sum {total}, checksum {check}")
    total = check = 0
    for a in range(6):
        m = [316, 1, 100000, 250, 400, 300][a]
        n = [316, 100000, 1, 400, 250, 333][a]
        x = [1, 7, 2, 100, 1, 3][a]
        answer = min_operations(random_grid(m, n, x, 10000, a < 5), x)
        total += answer
        check = mix(check, answer)
    print(f"6 grids of 100000 values: sum {total}, checksum {check}")


main()
