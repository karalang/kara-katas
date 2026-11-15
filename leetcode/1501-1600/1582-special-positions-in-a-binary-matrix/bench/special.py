# LeetCode #1582 bench: the same row and column sums, in Python.


def num_special(mat):
    n = len(mat[0])
    rows = [sum(row) for row in mat]
    cols = [sum(row[j] for row in mat) for j in range(n)]
    return sum(
        sum(1 for j in range(n) if row[j] == 1 and rows[i] == 1 and cols[j] == 1)
        for i, row in enumerate(mat)
    )


seed = 1582


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    mats = []
    for _ in range(2000):
        mats.append([[1 if next_random() % 100 == 0 else 0 for _ in range(100)] for _ in range(100)])
    check = 0
    total = 0
    for mat in mats:
        special = num_special(mat)
        total += special
        check = mix(check, special)
    print(f"2000 matrices of 100 x 100: special positions {total}, checksum {check}")


main()
