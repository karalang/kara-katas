# LeetCode #931: Minimum Falling Path Sum -- bench: one row of sums at a
# time. Mirrors min_falling_path_sum.kara.


def min_falling_path_sum(matrix):
    n = len(matrix)
    prev = list(matrix[0])
    for r in range(1, n):
        row = matrix[r]
        cur = [0] * n
        for c in range(n):
            best = prev[c]
            if c > 0 and prev[c - 1] < best:
                best = prev[c - 1]
            if c + 1 < n and prev[c + 1] < best:
                best = prev[c + 1]
            cur[c] = row[c] + best
        prev = cur
    answer = prev[0]
    for v in prev:
        if v < answer:
            answer = v
    return answer


seed = 931


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 150, 100, 100
    # count matrices of n x n values from -100 to 100, built once
    matrices = []
    for _ in range(count):
        matrices.append([[next_random() % 201 - 100 for _ in range(n)] for _ in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        # each round visits every matrix, starting from a different one
        for i in range(count):
            a = min_falling_path_sum(matrices[(r + i) % count])
            total += a
            check = (check * 1000003 + a + 1000000) % 1000000007
    print(f"{rounds} rounds over {count} matrices of {n} x {n}: answers summing to {total}, checksum {check}")


main()
