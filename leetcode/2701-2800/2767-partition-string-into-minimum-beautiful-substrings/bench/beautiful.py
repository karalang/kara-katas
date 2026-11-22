# LeetCode #2767: Partition String Into Minimum Beautiful Substrings --
# the bench in Python: the ★ arm over 100000 strings of 15 binary digits,
# all drawn first, then each answered 5 times.


def is_power_of_five(v):
    while v > 1 and v % 5 == 0:
        v //= 5
    return v == 1


def minimum_beautiful_substrings(s):
    n = len(s)
    best = [-1] * (n + 1)
    best[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            if best[j] < 0 or s[j] != "1":
                continue
            if is_power_of_five(int(s[j:i], 2)):
                if best[i] < 0 or best[j] + 1 < best[i]:
                    best[i] = best[j] + 1
    return best[n]


seed = 2767


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 100000
    rounds = 5
    powers = ["1", "101", "11001", "1111101", "1001110001", "110000110101", "11110100001001"]
    strings = []
    for _ in range(count):
        s = ""
        while True:
            p = powers[next_random() % 7]
            if len(s) + len(p) > 15:
                break
            s += p
        while len(s) < 15:
            s += "1" if next_random() % 2 == 1 else "0"
        if next_random() % 2 == 1:
            k = next_random() % 15
            s = s[:k] + ("0" if s[k] == "1" else "1") + s[k + 1:]
        strings.append(s)
    split = pieces = check = 0
    for r in range(rounds):
        for s in strings:
            a = minimum_beautiful_substrings(s)
            if a > 0:
                split += 1
                pieces += a
            check = (check * 31 + a + 1 + r) % 1000000007
    print(f"{count} strings of 15, {rounds} rounds: {split} split, pieces sum to {pieces}, checksum {check}")


main()
