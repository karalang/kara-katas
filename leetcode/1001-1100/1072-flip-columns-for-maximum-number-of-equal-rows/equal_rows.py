# LeetCode #1072: Flip Columns For Maximum Number of Equal Rows -- the Python
# mirror of equal_rows.kara (the ★ arm): each row read as its pattern, the
# row flipped where its first cell is 1, and the most rows sharing one.


def max_equal_rows(matrix):
    counts = {}
    best = 0
    for row in matrix:
        key = "".join("1" if c != row[0] else "0" for c in row)
        counts[key] = counts.get(key, 0) + 1
        best = max(best, counts[key])
    return best


seed = 1072


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_bits(n):
    return [next_random() % 2 for _ in range(n)]


def random_matrix(rows, cols):
    # one to three patterns; each row is one of them, its complement, or one
    # time in four a row of its own
    m = next_random() % rows + 1
    n = next_random() % cols + 1
    patterns = [random_bits(n) for _ in range(next_random() % 3 + 1)]
    matrix = []
    for _ in range(m):
        roll = next_random() % 8
        if roll < 2:
            matrix.append(random_bits(n))
        else:
            p = patterns[next_random() % len(patterns)]
            matrix.append([1 - c for c in p] if roll < 5 else list(p))
    return matrix


def main():
    examples = [
        [[0, 1], [1, 1]],
        [[0, 1], [1, 0]],
        [[0, 0, 0], [0, 0, 1], [1, 1, 0]],
        [[1]],
        [[0, 0], [0, 0], [1, 1]],
        [[0, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]],
        [[1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [0, 0, 0, 0], [1, 1, 1, 1]],
        [[0, 1, 1, 0, 1], [1, 1, 0, 0, 1], [0, 0, 1, 1, 0]],
        [[1, 1, 1], [0, 1, 1], [1, 0, 0], [0, 0, 0], [1, 1, 0]],
    ]
    for matrix in examples:
        print(f"{' '.join(''.join(str(c) for c in row) for row in matrix)} -> {max_equal_rows(matrix)}")
    for count, rows, cols, label in [(3000, 8, 6, "3000 matrices up to 8 by 6"), (40, 300, 300, "40 matrices up to 300 by 300")]:
        total = check = 0
        for _ in range(count):
            x = max_equal_rows(random_matrix(rows, cols))
            total += x
            check = (check * 31 + x) % 1000000007
        print(f"{label}: answers sum {total}, checksum {check}")
    zeros = [[0] * 300 for _ in range(300)]
    stripes = [[(i + j) % 2 for j in range(300)] for i in range(300)]
    counting = [[(i >> j) & 1 for j in range(9)] for i in range(300)]
    single = [[(i >> j) & 1 for j in range(9)] for i in range(1)]
    print(f"300 by 300 of zeros: {max_equal_rows(zeros)}")
    print(f"300 by 300 of stripes: {max_equal_rows(stripes)}")
    print(f"0 to 299 in 9 bits: {max_equal_rows(counting)}")
    print(f"one row of 9 zeros: {max_equal_rows(single)}")


main()
