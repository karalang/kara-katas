# LeetCode #2326: Spiral Matrix IV -- the bench, the ★ arm in Python. A
# walker starts at the top left heading right and writes the list's
# values one by one, turning clockwise when the next cell is off the grid
# or already written. O(m n).


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def spiral_matrix(m, n, head):
    grid = [[-1] * n for _ in range(m)]
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c, d = 0, 0, 0
    node = head
    while node is not None:
        grid[r][c] = node.val
        nr, nc = r + moves[d][0], c + moves[d][1]
        if nr < 0 or nr >= m or nc < 0 or nc >= n or grid[nr][nc] != -1:
            d = (d + 1) % 4
        r += moves[d][0]
        c += moves[d][1]
        node = node.next
    return grid


seed = 2326


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rows = [100, 200, 250, 400, 500, 1000, 50, 125, 80, 160]
    heads = []
    for k in range(10):
        head = None
        for _ in range(90000 + 1111 * k):
            head = ListNode(next_random() % 1001, head)
        heads.append(head)
    check = 0
    for p in range(30):
        for k in range(10):
            m = rows[(p + k) % 10]
            n = 100000 // m
            grid = spiral_matrix(m, n, heads[k])
            check = (check * 31 + grid[p % m][(3 * p + k) % n] + grid[m // 2][n // 2] + 2) % 1000000007
    print(f"30 passes over 10 lists in grids of 10^5 cells: checksum {check}")


main()
