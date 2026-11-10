# LeetCode #2056: Number of Valid Move Combinations On Chessboard -- Python
# mirror of the ★ arm (moves.kara): each piece's moves listed, staying put
# one of them, and the pieces given moves one at a time by backtracking,
# each new move walked against the moves already chosen. Output is
# byte-identical to the Kāra arms.


def moves_of(kind, r, c):
    dirs = []
    if kind != "bishop":
        dirs += [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if kind != "rook":
        dirs += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    moves = [(0, 0, 0)]
    for dr, dc in dirs:
        steps = 1
        while 1 <= r + dr * steps <= 8 and 1 <= c + dc * steps <= 8:
            moves.append((dr, dc, steps))
            steps += 1
    return moves


def collide(a, ma, b, mb):
    for t in range(1, max(ma[2], mb[2]) + 1):
        ta, tb = min(t, ma[2]), min(t, mb[2])
        if a[0] + ma[0] * ta == b[0] + mb[0] * tb and a[1] + ma[1] * ta == b[1] + mb[1] * tb:
            return True
    return False


def count_combinations(pieces, positions):
    options = [moves_of(pieces[i], *positions[i]) for i in range(len(pieces))]
    chosen = []

    def count_from(i):
        if i == len(positions):
            return 1
        total = 0
        for m in options[i]:
            if all(not collide(positions[j], chosen[j], positions[i], m) for j in range(i)):
                chosen.append(m)
                total += count_from(i + 1)
                chosen.pop()
        return total

    return count_from(0)


# ---- test harness ---------------------------------------------------------

seed = 2056


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, rows, cols):
    kinds = ["rook", "queen", "bishop"]
    pieces, positions = [], []
    while len(positions) < n:
        r = next_random() % rows + 1
        c = next_random() % cols + 1
        kind = kinds[next_random() % 3]
        if (r, c) not in positions:
            pieces.append(kind)
            positions.append((r, c))
    return pieces, positions


def show(xs):
    return "[" + ", ".join(xs) + "]"


def main():
    examples = [
        (["rook"], [(1, 1)]),
        (["queen"], [(1, 1)]),
        (["bishop"], [(4, 3)]),
        (["rook", "rook"], [(1, 1), (8, 8)]),
        (["queen", "bishop"], [(5, 7), (3, 4)]),
        (["rook", "rook"], [(1, 1), (1, 2)]),
        (["queen", "queen", "rook"], [(4, 4), (4, 5), (5, 4)]),
    ]
    for pieces, positions in examples:
        shown = show(f"({r}, {c})" for r, c in positions)
        print(f"{show(pieces)} {shown} -> {count_combinations(pieces, positions)}")
    total = check = 0
    for _ in range(300):
        n = next_random() % 3 + 1
        side = next_random() % 6 + 3
        count = count_combinations(*draw(n, side, side))
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"300 boards: sum {total}, checksum {check}")
    total = check = 0
    for _ in range(4):
        count = count_combinations(*draw(4, 8, 8))
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"4 boards of 4: sum {total}, checksum {check}")


main()
