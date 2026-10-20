# Benchmark for #816: Ambiguous Coordinates -- mirror of the ★ arm (every
# split and every point), with the same workload as
# ambiguous_coordinates.kara.


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


seed = 816


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 64, 400000
    strings = []
    for _ in range(count):
        strings.append([0 if next_random() % 4 == 0 else next_random() % 10 for _ in range(10)])
    total = 0
    checksum = 0
    for rnd in range(rounds):
        g = rnd % count
        at = next_random() % 10
        strings[g][at] = 0 if next_random() % 4 == 0 else next_random() % 10
        s = "(" + "".join(f"{d}" for d in strings[g]) + ")"
        answer = ambiguous_coordinates(s)
        total += len(answer)
        for c in answer:
            checksum = (checksum * 131 + len(c)) % 1000000007
    print(f"{rounds} rounds of 10 digits: {total} coordinates, checksum {checksum}")


main()
