# LeetCode #1643: Kth Smallest Instructions -- the bench's Python mirror:
# the ★ arm on 1000000 random destinations of 1 to 15 rows and columns,
# each with a k drawn from all of its paths, all drawn first.

CASES = 1000000


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


cases = []
for _ in range(CASES):
    row = next_random() % 15 + 1
    column = next_random() % 15 + 1
    k = (next_random() * 32768 + next_random()) % count_paths(row, column) + 1
    cases.append((row, column, k))
check = 0
total = 0
for row, column, k in cases:
    path = kth_smallest_path([row, column], k)
    total += path.index("V")
    for b in path:
        check = (check * 3 + (1 if b == "H" else 2)) % 1000000007
print(f"{CASES} destinations of up to 15 by 15: first moves down sum to {total}, checksum {check}")
