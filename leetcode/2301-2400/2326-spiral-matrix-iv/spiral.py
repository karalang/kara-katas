# LeetCode #2326: Spiral Matrix IV -- the ★ arm in Python. A walker starts
# at the top left heading right and writes the list's values one by one;
# when the next cell is off the grid or already written, it turns
# clockwise. Cells never reached keep -1. O(m n).


class ListNode:
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


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def show(grid):
    return "[" + ",".join("[" + ",".join(str(v) for v in row) + "]" for row in grid) + "]"


def fold(grid, acc):
    for row in grid:
        for v in row:
            acc[0] = (acc[0] * 31 + v + 1) % 1000000007
            if v == -1:
                acc[1] += 1


def main():
    print(show(spiral_matrix(3, 5, build([3, 0, 2, 6, 8, 1, 7, 9, 4, 2, 5, 5, 0]))))
    print(show(spiral_matrix(1, 4, build([0, 1, 2]))))
    print(show(spiral_matrix(1, 1, build([7]))))
    print(show(spiral_matrix(5, 1, build([1, 2, 3]))))
    print(show(spiral_matrix(4, 4, build(list(range(1, 17))))))
    values = [next_random() % 1001 for _ in range(50000)]
    acc = [0, 0]
    fold(spiral_matrix(300, 300, build(values)), acc)
    print(f"300 by 300: checksum {acc[0]}, {acc[1]} empty")
    acc = [0, 0]
    for _ in range(1000):
        m = next_random() % 8 + 1
        n = next_random() % 8 + 1
        length = next_random() % (m * n) + 1
        values = [next_random() % 1001 for _ in range(length)]
        fold(spiral_matrix(m, n, build(values)), acc)
    print(f"1000 grids: checksum {acc[0]}, {acc[1]} empty")


main()
