# LeetCode 777 — Swap Adjacent in LR String: Python mirror of the ★ arm
# (two pointers), with the same harness.


def can_transform(start, end):
    s = start.encode()
    e = end.encode()
    n = len(s)
    if len(e) != n:
        return False
    i = 0
    j = 0
    while True:
        while i < n and s[i] == ord("X"):
            i += 1
        while j < n and e[j] == ord("X"):
            j += 1
        if i == n or j == n:
            return i == n and j == n
        if s[i] != e[j]:
            return False
        if s[i] == ord("L") and i < j:
            return False
        if s[i] == ord("R") and i > j:
            return False
        i += 1
        j += 1


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_text(seed, n, x_in_4):
    out = []
    for _ in range(n):
        r = next_random(seed) % 8
        if r < 2 * x_in_4:
            out.append("X")
        elif r % 2 == 0:
            out.append("L")
        else:
            out.append("R")
    return "".join(out)


def moved(seed, text, moves):
    b = list(text)
    n = len(b)
    for _ in range(moves):
        if n < 2:
            break
        i = next_random(seed) % (n - 1)
        if b[i] == "X" and b[i + 1] == "L":
            b[i], b[i + 1] = "L", "X"
        elif b[i] == "R" and b[i + 1] == "X":
            b[i], b[i + 1] = "X", "R"
    return "".join(b)


def show(start, end):
    answer = can_transform(start, end)
    print(f'"{start}" -> "{end}": {str(answer).lower()}')


def main():
    show("RXXLRXRXL", "XRLXXRRLX")
    show("X", "L")
    show("LXXLXRLXXL", "XLLXRXLXLX")
    show("XXXXXLXXXX", "LXXXXXXXXX")
    show("XXRXXLXXXX", "XXXXRXXLXX")
    show("RL", "LR")
    show("XL", "LX")
    show("RX", "XR")
    show("LX", "XL")
    show("XLR", "LXR")
    seed = [777]
    big = random_text(seed, 10000, 2)
    far = moved(seed, big, 400000)
    print(f"10000 letters, 400000 moves -> {str(can_transform(big, far)).lower()}")
    wrong = list(big)
    k = 0
    while not (wrong[k] == "L" and wrong[k + 1] == "X"):
        k += 1
    wrong[k], wrong[k + 1] = wrong[k + 1], wrong[k]
    print(f"10000 letters, an L a place right -> {str(can_transform(big, ''.join(wrong))).lower()}")
    yes = 0
    check = 0
    for case in range(300):
        n = 1 + next_random(seed) % 40
        start = random_text(seed, n, 1 + next_random(seed) % 3)
        if case % 2 == 0:
            end = moved(seed, start, next_random(seed) % (4 * n))
        else:
            end = random_text(seed, n, 2)
        answer = can_transform(start, end)
        if answer:
            yes += 1
        check = (check * 31 + (n if answer else 100 - n)) % 1000000007
    print(f"300 random pairs: {yes} reachable, checksum {check}")


main()
