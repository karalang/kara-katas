# LeetCode #631: Design Excel Sum Formula -- Python mirror of the ★ arm.
#
# A formula is a map from each cell it reads to how many times; reading
# a formula cell sums the cells it reads, each read the same way.


class Excel:
    def __init__(self, height, width):
        self.width = ord(width) - ord("A") + 1
        self.numbers = [0] * (height * self.width)
        self.formulas = [None] * (height * self.width)

    def set(self, row, column, val):
        at = self.cell(row, column)
        self.numbers[at] = val
        self.formulas[at] = None

    def get(self, row, column):
        return self.value(self.cell(row, column))

    def sum(self, row, column, numbers):
        at = self.cell(row, column)
        reads = {}
        for name in numbers:
            ends = name.split(":")
            top, left = self.position(ends[0])
            bottom, right = self.position(ends[-1])
            for r in range(top, bottom + 1):
                for c in range(left, right + 1):
                    source = r * self.width + c
                    reads[source] = reads.get(source, 0) + 1
        self.formulas[at] = reads
        return self.value(at)

    def cell(self, row, column):
        return (row - 1) * self.width + (ord(column) - ord("A"))

    def position(self, name):
        return int(name[1:]) - 1, ord(name[0]) - ord("A")

    def value(self, at):
        if self.formulas[at] is None:
            return self.numbers[at]
        return sum(times * self.value(source) for source, times in self.formulas[at].items())


seed = 631


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter(index):
    return chr(ord("A") + index)


def main():
    excel = Excel(3, "C")
    excel.set(1, "A", 2)
    print(f"sum(3, C, [A1, A1:B2]) -> {excel.sum(3, 'C', ['A1', 'A1:B2'])}")
    excel.set(2, "B", 2)
    print(f"get(3, C) -> {excel.get(3, 'C')}")
    excel.set(1, "B", 5)
    print(f"sum(3, B, [C3, B1]) -> {excel.sum(3, 'B', ['C3', 'B1'])}")
    excel.set(1, "A", -3)
    print(f"get(3, B) -> {excel.get(3, 'B')}, get(3, C) -> {excel.get(3, 'C')}")
    excel.set(3, "C", 10)
    print(f"get(3, B) -> {excel.get(3, 'B')}")
    print(f"sum(3, A, [A1:C1, B1, B1:B1]) -> {excel.sum(3, 'A', ['A1:C1', 'B1', 'B1:B1'])}")
    excel.set(1, "C", -7)
    print(f"get(3, A) -> {excel.get(3, 'A')}")
    sheet = Excel(26, "Z")
    checksum = 0
    sums = 0
    for _ in range(400):
        kind = next_random() % 3
        row = 1 + next_random() % 26
        column = letter(next_random() % 26)
        result = 0
        if kind == 0:
            sheet.set(row, column, next_random() % 2001 - 1000)
        elif kind == 1 and row > 1:
            ranges = []
            for _ in range(1 + next_random() % 3):
                top = 1 + next_random() % (row - 1)
                left = next_random() % 26
                bottom = min(top + next_random() % 2, row - 1)
                right = min(left + next_random() % 2, 25)
                if top == bottom and left == right:
                    ranges.append(f"{letter(left)}{top}")
                else:
                    ranges.append(f"{letter(left)}{top}:{letter(right)}{bottom}")
            result = sheet.sum(row, column, ranges)
            sums += 1
        else:
            result = sheet.get(row, column)
        checksum = ((checksum * 31 + result) % 1000000007 + 1000000007) % 1000000007
    total = sum(sheet.get(row, letter(c)) for row in range(1, 27) for c in range(26))
    print(f"400 random operations ({sums} sums): checksum {checksum}, sheet total {total}")


main()
