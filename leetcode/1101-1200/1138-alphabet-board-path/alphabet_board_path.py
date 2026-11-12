# LeetCode #1138: Alphabet Board Path -- the mirror of the ★ arm:
# coordinates, up and left first, down and right after.


def alphabet_board_path(target):
    path = []
    row = col = 0
    for c in target:
        k = ord(c) - ord("a")
        r, k_col = k // 5, k % 5
        path.append("U" * max(row - r, 0))
        path.append("L" * max(col - k_col, 0))
        path.append("D" * max(r - row, 0))
        path.append("R" * max(k_col - col, 0))
        path.append("!")
        row, col = r, k_col
    return "".join(path)


seed = 1138


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


BOARD = ["abcde", "fghij", "klmno", "pqrst", "uvwxy", "z"]


def walk(path):
    row = col = 0
    spelled = []
    for m in path:
        if m == "U":
            row -= 1
        elif m == "D":
            row += 1
        elif m == "L":
            col -= 1
        elif m == "R":
            col += 1
        elif m == "!":
            spelled.append(BOARD[row][col])
        else:
            return f"a move '{m}'"
        if row < 0 or row >= len(BOARD) or col < 0 or col >= len(BOARD[row]):
            return f"off the board at row {row}, column {col}"
    return "".join(spelled)


def canonical(path):
    out = []
    count = {"U": 0, "L": 0, "D": 0, "R": 0}
    for m in path:
        if m in count:
            count[m] += 1
        else:
            for name in "ULDR":
                out.append(name * count[name])
                count[name] = 0
            out.append(m)
    return "".join(out)


def show(target):
    path = alphabet_board_path(target)
    spelled = walk(path)
    verdict = "spells it" if spelled == target else f"spells {spelled}"
    print(f"{target} -> length {len(path)}, {verdict}: {canonical(path)}")


def main():
    for target in ["leet", "code", "a", "e", "z", "zz", "za", "az", "zdz", "yz", "zy", "uzu", "zez"]:
        show(target)
    show("abcdefghijklmnopqrstuvwxyz")
    show("zyxwvutsrqponmlkjihgfedcba")
    letters = "abcdefghijklmnopqrstuvwxyz"
    total = wrong = check = 0
    for _ in range(2000):
        n = next_random() % 100 + 1
        target = "".join(letters[next_random() % 26] for _ in range(n))
        path = alphabet_board_path(target)
        total += len(path)
        if walk(path) != target:
            wrong += 1
        for c in canonical(path):
            check = (check * 131 + ord(c)) % 1000000007
    print(f"2000 random targets: lengths total {total}, {wrong} wrong, checksum {check}")
    for target in ["z" * 100, "az" * 50, "ez" * 50, "ya" * 50]:
        path = alphabet_board_path(target)
        ok = "true" if walk(path) == target else "false"
        print(f"{len(target)} letters from {target[:2]}: length {len(path)}, spells it {ok}")


main()
