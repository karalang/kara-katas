# LeetCode #931: Minimum Falling Path Sum -- one row of sums at a time
# (Python mirror).


def min_falling_path_sum(matrix):
    n = len(matrix)
    prev = list(matrix[0])
    for r in range(1, n):
        cur = [0] * n
        for c in range(n):
            best = prev[c]
            if c > 0 and prev[c - 1] < best:
                best = prev[c - 1]
            if c + 1 < n and prev[c + 1] < best:
                best = prev[c + 1]
            cur[c] = matrix[r][c] + best
        prev = cur
    return min(prev)


seed = 931


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, matrix):
    print(f"{name}: {min_falling_path_sum(matrix)}")


def random_matrix(n, lo, hi):
    return [[lo + next_random() % (hi - lo + 1) for _ in range(n)] for _ in range(n)]


def main():
    show("example 1", [[2, 1, 3], [6, 5, 4], [7, 8, 9]])
    show("example 2", [[-19, 57], [-40, -5]])
    show("one cell", [[-7]])
    show("opposite corners", [[0, 9, 9, -5], [9, 9, 9, 9], [9, 9, 9, 9], [-5, 9, 9, 0]])
    show("zigzag", [[1, 50, 50, 50], [50, 1, 50, 50], [50, 50, 1, 50], [50, 1, 50, 50]])
    show("down an edge", [[-1, 0, 0], [-1, 0, 0], [-1, 0, 0]])
    show("all 100", [[100, 100], [100, 100]])
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 60
        matrix = random_matrix(n, -100, 100)
        a = min_falling_path_sum(matrix)
        total += a
        check = (check * 1000003 + a + 1000000) % 1000000007
    print(f"300 random matrices: answers summing to {total}, checksum {check}")
    big = random_matrix(100, -100, 100)
    low = [[-100] * 100 for _ in range(100)]
    board = [[-100 if (r + c) % 2 == 0 else 100 for c in range(100)] for r in range(100)]
    a = min_falling_path_sum(big)
    b = min_falling_path_sum(low)
    c = min_falling_path_sum(board)
    print(f"100 x 100: random {a}, all -100 {b}, checkerboard {c}")


main()
