# LeetCode 761 — Special Binary String: benchmark, the ★ arm in Python.
# 200,000 random special strings of 50 characters.


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


def main():
    seed = 761

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    rounds = 200000
    leading = 0
    check = 0
    for _ in range(rounds):
        s = []
        ones = depth = 0
        for _ in range(50):
            if ones < 25 and (depth == 0 or next_random() % 2 == 0):
                s.append("1")
                ones += 1
                depth += 1
            else:
                s.append("0")
                depth -= 1
        s = "".join(s)
        largest = make_largest_special(s)
        ones = True
        for c in largest:
            if c == "0":
                ones = False
            if ones:
                leading += 1
            check = (check * 2 + (1 if c == "1" else 0)) % 1000000007
    print(f"{rounds} strings of 50 characters: {leading} leading 1s, checksum {check}")


main()
