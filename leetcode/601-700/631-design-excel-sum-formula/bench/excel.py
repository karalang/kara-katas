# LeetCode 631 -- Design Excel Sum Formula, bench mirror in Python.
#
# The rebuild arm of excel.kara: every formula is the list of cells it
# reads, and after each write a depth-first walk orders the formula
# cells and recomputes them all. Same 2,000 operations, same 60 rounds,
# same output line.
import sys

sys.setrecursionlimit(10000)


class Excel:
    def __init__(self, height, width):
        columns = ord(width) - ord("A") + 1
        self.width = columns
        self.values = [0] * (height * columns)
        self.formulas = [None] * (height * columns)

    def set(self, row, column, val):
        at = self.cell(row, column)
        self.values[at] = val
        self.formulas[at] = None
        self.recompute()

    def get(self, row, column):
        return self.values[self.cell(row, column)]

    def sum(self, row, column, numbers):
        at = self.cell(row, column)
        reads = []
        for rng in numbers:
            ends = rng.split(":")
            top, left = self.position(ends[0])
            bottom, right = self.position(ends[-1])
            for r in range(top, bottom + 1):
                for c in range(left, right + 1):
                    reads.append(r * self.width + c)
        self.formulas[at] = reads
        self.recompute()
        return self.values[at]

    def cell(self, row, column):
        return (row - 1) * self.width + (ord(column) - ord("A"))

    # The zero-based row and column of a name such as `B12`.
    def position(self, name):
        return int(name[1:]) - 1, ord(name[0]) - ord("A")

    def recompute(self):
        seen = [False] * len(self.values)
        order = []
        for at in range(len(self.values)):
            visit(self.formulas, at, seen, order)
        for at in order:
            reads = self.formulas[at]
            if reads is not None:
                total = 0
                for source in reads:
                    total += self.values[source]
                self.values[at] = total


# Append `at` to `order` after every cell its formula reads.
def visit(formulas, at, seen, order):
    if seen[at]:
        return
    seen[at] = True
    reads = formulas[at]
    if reads is not None:
        for source in reads:
            visit(formulas, source, seen, order)
    order.append(at)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def letter(index):
    return chr(ord("A") + index)


def make_ops(count, seed):
    ops = []
    for _ in range(count):
        kind = next_random(seed) % 3
        row = 1 + next_random(seed) % 26
        column = letter(next_random(seed) % 26)
        val = 0
        ranges = []
        if kind == 0:
            val = next_random(seed) % 2001 - 1000
        elif kind == 1 and row > 1:
            for _ in range(1 + next_random(seed) % 3):
                top = 1 + next_random(seed) % (row - 1)
                left = next_random(seed) % 26
                bottom = min(top + next_random(seed) % 2, row - 1)
                right = min(left + next_random(seed) % 2, 25)
                if top == bottom and left == right:
                    ranges.append(f"{letter(left)}{top}")
                else:
                    ranges.append(f"{letter(left)}{top}:{letter(right)}{bottom}")
        else:
            kind = 2
        ops.append((kind, row, column, val, ranges))
    return ops


def main():
    seed = [631]
    ops = make_ops(2000, seed)
    rounds = 60
    sums = checksum = total = 0
    for _ in range(rounds):
        sheet = Excel(26, "Z")
        for kind, row, column, val, ranges in ops:
            result = 0
            if kind == 0:
                sheet.set(row, column, val)
            elif kind == 1:
                result = sheet.sum(row, column, ranges)
                sums += 1
            else:
                result = sheet.get(row, column)
            checksum = ((checksum * 31 + result) % 1000000007 + 1000000007) % 1000000007
        for row in range(1, 27):
            for c in range(26):
                total += sheet.get(row, letter(c))
    print(f"{len(ops)} operations, {rounds} rounds ({sums} sums): checksum {checksum}, sheet total {total}")


main()
