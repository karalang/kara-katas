# LeetCode #1284: Minimum Number of Flips to Convert Binary Matrix to Zero
# Matrix -- bench, in Python: the ★ arm (breadth-first search over bit masks)
# on every matrix of every shape, 1 by 1 to 3 by 3, 3000 rounds.
from collections import deque


def min_flips(mat):
    rows, cols = len(mat), len(mat[0])
    cells = rows * cols
    start = 0
    flip = []
    for i in range(rows):
        for j in range(cols):
            if mat[i][j] == 1:
                start |= 1 << (i * cols + j)
            mask = 1 << (i * cols + j)
            if i > 0:
                mask |= 1 << ((i - 1) * cols + j)
            if i + 1 < rows:
                mask |= 1 << ((i + 1) * cols + j)
            if j > 0:
                mask |= 1 << (i * cols + j - 1)
            if j + 1 < cols:
                mask |= 1 << (i * cols + j + 1)
            flip.append(mask)
    dist = [-1] * (1 << cells)
    dist[start] = 0
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if state == 0:
            return dist[state]
        for mask in flip:
            nxt = state ^ mask
            if dist[nxt] < 0:
                dist[nxt] = dist[state] + 1
                queue.append(nxt)
    return -1


def matrix(rows, cols, bits):
    return [[(bits >> (i * cols + j)) & 1 for j in range(cols)] for i in range(rows)]


def main():
    check = 0
    for rnd in range(3000):
        for rows in range(1, 4):
            for cols in range(1, 4):
                for bits in range(1 << (rows * cols)):
                    check = (check * 131 + min_flips(matrix(rows, cols, bits)) + rnd + 2) % 1000000007
    print(f"3000 rounds of every matrix: checksum {check}")


if __name__ == "__main__":
    main()
