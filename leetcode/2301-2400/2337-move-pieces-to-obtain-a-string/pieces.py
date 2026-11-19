# LeetCode #2337: Move Pieces to Obtain a String -- the Python mirror of
# the ★ arm: two indices walking the start and the target together,
# each skipping blanks, the pieces matched in order and each `L` no
# later in the target, each `R` no earlier.


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


SEED = [2337]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def random_line(n):
    out = []
    for _ in range(n):
        r = next_random() % 4
        out.append("L" if r == 0 else "R" if r == 1 else "_")
    return "".join(out)


def moved(line, moves):
    cells = list(line)
    n = len(cells)
    for _ in range(moves):
        i = next_random() % n
        if cells[i] == "L" and i > 0 and cells[i - 1] == "_":
            cells[i - 1] = "L"
            cells[i] = "_"
        elif cells[i] == "R" and i + 1 < n and cells[i + 1] == "_":
            cells[i + 1] = "R"
            cells[i] = "_"
    return "".join(cells)


def show(b):
    return "true" if b else "false"


def main():
    print(show(can_change("_L__R__R_", "L______RR")))
    print(show(can_change("R_L_", "__LR")))
    print(show(can_change("_R", "R_")))
    print(show(can_change("____", "____")))
    print(show(can_change("R_L", "L_R")))
    print(show(can_change("L__", "__L")))
    start = random_line(2000)
    target = moved(start, 100000)
    print(show(can_change(start, target)))
    changed = list(target)
    blank = changed.index("_")
    changed[blank] = "L"
    print(show(can_change(start, "".join(changed))))
    check = 0
    yes = 0
    for _ in range(2000):
        n = next_random() % 10 + 1
        start = random_line(n)
        if next_random() % 2 == 0:
            moves = next_random() % 21
            target = moved(start, moves)
        else:
            target = random_line(n)
        can = can_change(start, target)
        check = (check * 31 + (2 if can else 1)) % 1000000007
        if can:
            yes += 1
    print(f"2000 cases: checksum {check}, {yes} reachable")


main()
