# LeetCode #1072: Flip Columns For Maximum Number of Equal Rows -- the
# benchmark's Python mirror of equal_rows.kara: the same count of row
# patterns over 200 matrices built once, each answered 30 times.


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
    matrices = [random_matrix(300, 300) for _ in range(200)]
    total = check = 0
    for _ in range(30):
        for matrix in matrices:
            x = max_equal_rows(matrix)
            total += x
            check = (check * 31 + x) % 1000000007
    print(f"6000 calls: answers sum {total}, checksum {check}")


main()
