"""LeetCode 305 - Number of Islands II.

Mirror of number_of_islands_ii.kara: union-find with union by rank and path
compression, carrying the island count incrementally. `parent[x] == -1` means
the cell is still water, so one array answers both the land/water question and
the forest.
"""


class DisjointSet:
    def __init__(self, n: int) -> None:
        self.parent = [-1] * n
        self.rank = [0] * n
        self.count = 0

    def is_land(self, x: int) -> bool:
        return self.parent[x] >= 0

    def add(self, x: int) -> None:
        self.parent[x] = x
        self.count += 1

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        cur = x
        while self.parent[cur] != root:
            nxt = self.parent[cur]
            self.parent[cur] = root
            cur = nxt
        return root

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        # Already the same island — merging again must NOT change the count.
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        self.count -= 1


def num_islands2(m: int, n: int, positions: list[tuple[int, int]]) -> list[int]:
    ds = DisjointSet(m * n)
    out = []
    for r, c in positions:
        idx = r * n + c
        # A repeated position is a no-op: the cell is already land.
        if not ds.is_land(idx):
            ds.add(idx)
            if r > 0 and ds.is_land(idx - n):
                ds.union(idx, idx - n)
            if r < m - 1 and ds.is_land(idx + n):
                ds.union(idx, idx + n)
            if c > 0 and ds.is_land(idx - 1):
                ds.union(idx, idx - 1)
            if c < n - 1 and ds.is_land(idx + 1):
                ds.union(idx, idx + 1)
        out.append(ds.count)
    return out


def report(m: int, n: int, flat: list[int]) -> None:
    positions = [(flat[i], flat[i + 1]) for i in range(0, len(flat) - 1, 2)]
    counts = num_islands2(m, n, positions)
    print(f"{m}x{n} -> " + " ".join(str(v) for v in counts))


def main() -> None:
    # The example from the LeetCode statement.
    report(3, 3, [0, 0, 0, 1, 1, 2, 2, 1])
    # A repeated position must not change the answer.
    report(3, 3, [0, 0, 0, 0, 0, 1, 0, 1])
    # One cell.
    report(1, 1, [0, 0])
    # A row filled left to right, then the gap that joins two runs.
    report(1, 5, [0, 0, 0, 2, 0, 4, 0, 1, 0, 3])
    # A column, same shape rotated.
    report(5, 1, [0, 0, 2, 0, 4, 0, 1, 0, 3, 0])
    # The centre of a plus closes four islands at once.
    report(3, 3, [0, 1, 1, 0, 1, 2, 2, 1, 1, 1])
    # Fill a 2x3 grid completely — must end at exactly one island.
    report(2, 3, [0, 0, 1, 1, 0, 2, 1, 0, 0, 1, 1, 2])
    # A ring around a hole never closes into one until the last cell.
    report(3, 3, [0, 0, 0, 1, 0, 2, 1, 2, 2, 2, 2, 1, 2, 0, 1, 0])


if __name__ == "__main__":
    main()
