# LeetCode #1246 bench, in Python: the ★ arm (interval dynamic
# programming, rows from the last) on 1000 random arrays of 100 values
# built once, each from 1 to v distinct values with v from 1 to 20, each
# asked twice; every answer folded into a checksum.


def minimum_moves(arr):
    n = len(arr)
    best = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            moves = 1 + best[i + 1][j]
            if i + 1 < j and arr[i + 1] == arr[i]:
                moves = min(moves, 1 + best[i + 2][j])
            for k in range(i + 2, j):
                if arr[k] == arr[i]:
                    moves = min(moves, best[i + 1][k] + best[k + 1][j])
            best[i][j] = moves
    return best[0][n]


seed = 1246


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(1000):
        values = next_random() % 20 + 1
        arrays.append([next_random() % values + 1 for _ in range(100)])
    check = 0
    for _ in range(2):
        for arr in arrays:
            check = (check * 131 + minimum_moves(arr)) % 1000000007
    print(f"2 rounds of 1000 arrays of 100 values: checksum {check}")


main()
