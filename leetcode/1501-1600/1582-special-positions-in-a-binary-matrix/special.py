# LeetCode #1582: Special Positions in a Binary Matrix -- the Python mirror
# of the ★ arm: the sum of each row and each column, then the ones whose
# row and column both sum to 1 counted. O(m n)


def num_special(mat):
    n = len(mat[0])
    rows = [sum(row) for row in mat]
    cols = [sum(row[j] for row in mat) for j in range(n)]
    return sum(
        sum(1 for j in range(n) if row[j] == 1 and rows[i] == 1 and cols[j] == 1)
        for i, row in enumerate(mat)
    )


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, sparse):
    check = 0
    total = 0
    for _ in range(count):
        m = next_random() % most + 1
        n = next_random() % most + 1
        odds = next_random() % sparse + 1
        mat = [[1 if next_random() % odds == 0 else 0 for _ in range(n)] for _ in range(m)]
        special = num_special(mat)
        total += special
        check = mix(check, special)
    print(f"{count} matrices of up to {most} x {most}: special positions {total}, checksum {check}")


def show(mat):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in mat) + "]"


def main():
    global seed
    examples = [
        [[1, 0, 0], [0, 0, 1], [1, 0, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[1]],
        [[0]],
        [[1, 1], [0, 0]],
        [[0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
    ]
    for mat in examples:
        print(f"{show(mat)} -> {num_special(mat)}")
    seed = 1582
    batch(3000, 5, 4)
    batch(300, 100, 100)
    batch(30, 100, 400)


main()
