# LeetCode #1727: Largest Submatrix With Rearrangements -- the bench
# (submatrix.kara): each row's column heights sorted, the k-th from the
# shortest giving a submatrix n - k wide.


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


def main():
    count = 20
    rounds = 50
    side = 316
    seed = [1727]
    problems = []
    for _ in range(count):
        matrix = []
        for _ in range(side):
            matrix.append([0 if next_random(seed) % 8 == 0 else 1 for _ in range(side)])
        problems.append(matrix)
    total = 0
    check = 0
    for r in range(rounds):
        for matrix in problems:
            answer = largest_submatrix(matrix)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} matrices of {side} by {side}, {rounds} rounds: areas sum to {total}, checksum {check}")


main()
