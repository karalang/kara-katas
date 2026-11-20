# LeetCode #1284: Minimum Number of Flips to Convert Binary Matrix to Zero
# Matrix -- Python mirror of the ★ arm: breadth-first search over bit masks.
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
    print(f"{min_flips([[0, 0], [0, 1]])} {min_flips([[0]])} {min_flips([[1, 0, 0], [1, 0, 0]])}")
    check = 0
    for rows in range(1, 4):
        for cols in range(1, 4):
            solvable = flips = most = 0
            for bits in range(1 << (rows * cols)):
                f = min_flips(matrix(rows, cols, bits))
                check = (check * 131 + f + 2) % 1000000007
                if f >= 0:
                    solvable += 1
                    flips += f
                    most = max(most, f)
            print(f"{rows} by {cols}: {solvable} of {1 << (rows * cols)} solvable, {flips} flips, at most {most}")
    print(f"checksum {check}")


if __name__ == "__main__":
    main()
