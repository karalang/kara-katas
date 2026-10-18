# LeetCode #699: Falling Squares -- bench program, Python mirror of the segment-tree arm.
from bisect import bisect_left

seed = 699


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class Tree:
    def __init__(self, cells):
        self.best = [0] * (4 * cells)
        self.pending = [-1] * (4 * cells)

    def push_down(self, node):
        p = self.pending[node]
        if p >= 0:
            for child in (2 * node, 2 * node + 1):
                self.best[child] = p
                self.pending[child] = p
            self.pending[node] = -1

    def query(self, node, lo, hi, frm, to):
        if to <= lo or hi <= frm:
            return 0
        if frm <= lo and hi <= to:
            return self.best[node]
        self.push_down(node)
        mid = (lo + hi) // 2
        return max(self.query(2 * node, lo, mid, frm, to), self.query(2 * node + 1, mid, hi, frm, to))

    def set(self, node, lo, hi, frm, to, h):
        if to <= lo or hi <= frm:
            return
        if frm <= lo and hi <= to:
            self.best[node] = h
            self.pending[node] = h
            return
        self.push_down(node)
        mid = (lo + hi) // 2
        self.set(2 * node, lo, mid, frm, to, h)
        self.set(2 * node + 1, mid, hi, frm, to, h)
        self.best[node] = max(self.best[2 * node], self.best[2 * node + 1])


def falling_squares(positions):
    edges = sorted({e for left, side in positions for e in (left, left + side)})
    cells = len(edges)
    tree = Tree(cells)
    answer = []
    for left, side in positions:
        frm = bisect_left(edges, left)
        to = bisect_left(edges, left + side)
        top = tree.query(1, 0, cells, frm, to) + side
        tree.set(1, 0, cells, frm, to, top)
        answer.append(tree.best[1])
    return answer


def main():
    problems = []
    for p in range(100):
        width = 1000 + p * 999990
        biggest = 1 + next_random() % 1000000
        positions = []
        for _ in range(1000):
            a = next_random()
            b = next_random()
            left = 1 + (a * 32768 + b) % width
            side = 1 + next_random() % biggest
            positions.append((left, side))
        problems.append(positions)
    rounds = 5
    total = 0
    checksum = 0
    for _ in range(rounds):
        for positions in problems:
            last = falling_squares(positions)[-1]
            total += last
            checksum = (checksum * 31 + last) % 1000000007
    print(f"{rounds} rounds of 100 problems of 1000 squares: tallest stacks sum to {total}, checksum {checksum}")


main()
