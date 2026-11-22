# LeetCode #2864: Maximum Odd Binary Number -- the bench, as odd.kara:
# 10000 strings of 100 bits, each answered 50 times, every answer folded
# into the checksum byte by byte.


def maximum_odd_binary_number(s):
    ones = s.count("1")
    zeros = len(s) - ones
    return "1" * (ones - 1) + "0" * zeros + "1"


seed = 2864


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 10000, 50, 100
    strings = []
    for _ in range(count):
        bits = ["1" if next_random() % 3 == 0 else "0" for _ in range(n)]
        bits[next_random() % n] = "1"
        strings.append("".join(bits))
    ones_total = 0
    check = 0
    for r in range(rounds):
        for s in strings:
            best = maximum_odd_binary_number(s)
            ones_total += best.count("1")
            h = (check + r) % 1000000007
            for b in best.encode():
                h = (h * 31 + b) % 1000000007
            check = h
    print(f"{count} strings of {n}, {rounds} rounds: {ones_total} ones, checksum {check}")


main()
