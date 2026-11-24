# LeetCode #1337: The K Weakest Rows in a Matrix -- Python mirror of the ★
# arm: each row's soldiers by binary search, (soldiers, row) sorted, the
# first k rows kept.


def soldiers(row):
    low, high = 0, len(row)
    while low < high:
        mid = (low + high) // 2
        if row[mid] == 1:
            low = mid + 1
        else:
            high = mid
    return low


def k_weakest_rows(mat, k):
    rows = sorted((soldiers(row), i) for i, row in enumerate(mat))
    return [i for _, i in rows[:k]]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(m, n, few):
    mat = []
    for _ in range(m):
        s = next_random() % (min(n, few) + 1)
        mat.append([1] * s + [0] * (n - s))
    return mat


def fold(check, rows):
    c = check
    for r in rows:
        c = (c * 131 + r) % 1000000007
    return (c * 131 + 7) % 1000000007


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    a = k_weakest_rows([[1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]], 3)
    b = k_weakest_rows([[1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0]], 2)
    print(f"{show(a)} {show(b)} {show(k_weakest_rows([[0, 0], [0, 0]], 2))} {show(k_weakest_rows([[1, 1], [1, 1], [1, 1]], 1))}")
    seed = 1337
    big = draw(100, 100, 100)
    al = k_weakest_rows(big, 100)
    print(f"100 by 100: weakest {show(k_weakest_rows(big, 5))}, strongest {al[99]}, checksum {fold(0, al)}")
    check = 0
    for t in range(300):
        big_one = t % 25 == 0
        m = 2 + next_random() % 99 if big_one else 2 + next_random() % 9
        n = 2 + next_random() % 99 if big_one else 2 + next_random() % 9
        few = 2 if t % 2 == 0 else 100
        mat = draw(m, n, few)
        k = 1 + next_random() % m
        check = fold(check, k_weakest_rows(mat, k))
    print(f"300 random matrices: checksum {check}")


main()
