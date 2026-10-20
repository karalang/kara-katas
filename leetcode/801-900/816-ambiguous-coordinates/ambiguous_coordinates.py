# LeetCode 816 — Ambiguous Coordinates, every split and every point (mirror of the ★ arm).


def ambiguous_coordinates(s):
    digits = s[1:-1]
    out = []
    for cut in range(1, len(digits)):
        lefts = numbers(digits[:cut])
        rights = numbers(digits[cut:])
        for x in lefts:
            for y in rights:
                out.append(f"({x}, {y})")
    return out


def numbers(part):
    found = []
    for point in range(1, len(part) + 1):
        whole = part[:point]
        fraction = part[point:]
        if (whole == "0" or not whole.startswith("0")) and not fraction.endswith("0"):
            found.append(whole if fraction == "" else f"{whole}.{fraction}")
    return found


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    answer = sorted(ambiguous_coordinates(s))
    listing = "" if not answer else ": " + " ".join(answer)
    print(f"s = {s} -> {len(answer)}{listing}")


def summary(s):
    answer = sorted(ambiguous_coordinates(s))
    check = 0
    for c in answer:
        for b in c.encode():
            check = (check * 131 + b) % 1000000007
    return len(answer), check


def main():
    global seed
    for s in ["(123)", "(0123)", "(00011)", "(100)", "(00)", "(000)", "(10)", "(1010)", "(0010)"]:
        show(s)
    for s in ["(1234567891)", "(1000000000)", "(0000000001)", "(1010101010)"]:
        count, check = summary(s)
        print(f"s = {s} -> {count}, checksum {check}")
    seed = 816
    total = 0
    every = 0
    for r in range(300):
        length = 2 + next_random() % 9
        s = "("
        for _ in range(length):
            d = 0 if next_random() % (2 + r % 3) == 0 else next_random() % 10
            s += f"{d}"
        s += ")"
        count, check = summary(s)
        total += count
        every = (every * 131 + check) % 1000000007
    print(f"300 random rounds of 2 to 10 digits: {total} coordinates, checksum {every}")


main()
