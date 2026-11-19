# LeetCode #1643: Kth Smallest Instructions -- the Python mirror of the ★
# arm: the paths that start with 'H' counted from Pascal's triangle, and k
# placed among them or past them, one move at a time.


def kth_smallest_path(destination, k):
    v, h = destination
    n = v + h
    choose = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        choose[i][0] = 1
        for j in range(1, i + 1):
            choose[i][j] = choose[i - 1][j - 1] + choose[i - 1][j]
    path = []
    for _ in range(n):
        starting_h = choose[h + v - 1][v]
        if k <= starting_h:
            path.append("H")
            h -= 1
        else:
            path.append("V")
            k -= starting_h
            v -= 1
    return "".join(path)


# ---- the harness: the same as every arm's ---------------------------------

seed = 1643


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count_paths(row, column):
    count = 1
    for i in range(1, row + 1):
        count = count * (column + i) // i
    return count


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        row = next_random() % most + 1
        column = next_random() % most + 1
        k = (next_random() * 32768 + next_random()) % count_paths(row, column) + 1
        path = kth_smallest_path([row, column], k)
        total += path.index("V")
        for b in path:
            check = (check * 3 + (1 if b == "H" else 2)) % 1000000007
    print(f"{count} destinations of up to {most} by {most}: first moves down sum to {total}, checksum {check}")


print(kth_smallest_path([2, 3], 1))
print(kth_smallest_path([2, 3], 2))
print(kth_smallest_path([2, 3], 3))
print(kth_smallest_path([1, 1], 2))
print(kth_smallest_path([15, 15], 155117520))
print(kth_smallest_path([1, 15], 1))
batch(3000, 3)
batch(3000, 15)
batch(100000, 15)
