# LeetCode 761 — Special Binary String: the ★ arm in Python, same output.


def make_largest_special(s):
    mountains = []
    depth = 0
    start = 0
    for i, c in enumerate(s):
        depth += 1 if c == "1" else -1
        if depth == 0:
            mountains.append("1" + make_largest_special(s[start + 1:i]) + "0")
            start = i + 1
    mountains.sort(reverse=True)
    return "".join(mountains)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_special(m):
    s = []
    ones = 0
    depth = 0
    for _ in range(2 * m):
        if ones < m and (depth == 0 or next_random() % 2 == 0):
            s.append("1")
            ones += 1
            depth += 1
        else:
            s.append("0")
            depth -= 1
    return "".join(s)


def show(s):
    print(f"{s} -> {make_largest_special(s)}")


def main():
    global seed
    for s in ["11011000", "10", "1100", "101100", "10101010", "110100",
              "1011011000", "1101001110001100"]:
        show(s)
    seed = 761
    changed = 0
    check = 0
    for _ in range(300):
        m = 1 + next_random() % 25
        s = random_special(m)
        largest = make_largest_special(s)
        if largest != s:
            changed += 1
        for c in largest:
            check = (check * 2 + (1 if c == "1" else 0)) % 1000000007
    print(f"300 random strings: {changed} changed, checksum {check}")


main()
