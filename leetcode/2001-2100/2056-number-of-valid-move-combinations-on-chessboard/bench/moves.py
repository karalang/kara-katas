# LeetCode #2056: Number of Valid Move Combinations On Chessboard -- Python
# mirror of the ★ arm's benchmark (moves.kara): the same 200 boards of 4
# pieces, the same moves and backtracking.

seed = 2056


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    kinds = ["rook", "queen", "bishop"]
    total = check = 0
    for _ in range(200):
        pieces, positions = [], []
        while len(positions) < 4:
            r = next_random() % 8 + 1
            c = next_random() % 8 + 1
            kind = kinds[next_random() % 3]
            if (r, c) not in positions:
                pieces.append(kind)
                positions.append((r, c))
        count = count_combinations(pieces, positions)
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"200 boards: sum {total}, checksum {check}")


main()
