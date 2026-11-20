# LeetCode #1727: Largest Submatrix With Rearrangements -- the Python
# mirror of the ★ arm, submatrix.kara: each row's column heights sorted,
# the k-th from the shortest giving a submatrix n - k wide.


def largest_submatrix(matrix):
    n = len(matrix[0])
    heights = [0] * n
    best = 0
    for row in matrix:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == 1 else 0
        ordered = sorted(heights)
        for k in range(n):
            best = max(best, ordered[k] * (n - k))
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def batch(count, most, seed):
    total = 0
    check = 0
    for _ in range(count):
        m = next_random(seed) % most + 1
        n = next_random(seed) % most + 1
        matrix = []
        for _ in range(m):
            matrix.append([0 if next_random(seed) % 4 == 0 else 1 for _ in range(n)])
        answer = largest_submatrix(matrix)
        total += answer
        check = (check * 31 + answer + m * n) % 1000000007
    print(f"{count} matrices of up to {most} by {most}: areas sum to {total}, checksum {check}")


def main():
    print(largest_submatrix([[0, 0, 1], [1, 1, 1], [1, 0, 1]]))
    print(largest_submatrix([[1, 0, 1, 0, 1]]))
    print(largest_submatrix([[1, 1, 0], [1, 0, 1]]))
    print(largest_submatrix([[0]]))
    print(largest_submatrix([[1] * 316 for _ in range(316)]))
    seed = [1727]
    batch(3000, 5, seed)
    batch(300, 50, seed)
    batch(5, 316, seed)


main()
