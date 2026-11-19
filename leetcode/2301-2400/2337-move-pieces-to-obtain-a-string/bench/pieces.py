# LeetCode #2337: Move Pieces to Obtain a String -- the bench, the ★ arm
# in Python: two indices walking the start and the target together, each
# skipping blanks, the pieces matched in order and each `L` no later in
# the target, each `R` no earlier.


def can_change(start, target):
    n = len(start)
    i = j = 0
    while True:
        while i < n and start[i] == "_":
            i += 1
        while j < n and target[j] == "_":
            j += 1
        if i == n or j == n:
            return i == n and j == n
        if start[i] != target[j]:
            return False
        if start[i] == "L" and i < j:
            return False
        if start[i] == "R" and i > j:
            return False
        i += 1
        j += 1


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    pairs = []
    for q in range(10):
        cells = []
        for i in range(100000):
            r = scrambled(q * 100000 + i) % 4
            cells.append("L" if r == 0 else "R" if r == 1 else "_")
        start = "".join(cells)
        for _ in range(3):
            for i in range(1, 100000):
                if cells[i] == "L" and cells[i - 1] == "_":
                    cells[i - 1] = "L"
                    cells[i] = "_"
            for i in range(99998, -1, -1):
                if cells[i] == "R" and cells[i + 1] == "_":
                    cells[i + 1] = "R"
                    cells[i] = "_"
        if q % 2 == 1:
            first = next(k for k, c in enumerate(cells) if c != "_")
            cells[first] = "R" if cells[first] == "L" else "L"
        pairs.append((start, "".join(cells)))
    check = 0
    for p in range(10):
        for start, target in pairs:
            can = can_change(start, target)
            check = (check * 31 + (2 if can else 1) + p) % 1000000007
    print(f"10 passes over 10 pairs of 10^5 places: checksum {check}")


main()
