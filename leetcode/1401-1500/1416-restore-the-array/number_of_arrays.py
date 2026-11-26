# LeetCode #1416, Python mirror of number_of_arrays.kara: ways[i] counts
# the arrays the digits from i on can be read as, each number with no
# leading 0 and at most k followed by any array of the rest.

MODULUS = 1000000007


def number_of_arrays(s, k):
    n = len(s)
    ways = [0] * (n + 1)
    ways[n] = 1
    for i in range(n - 1, -1, -1):
        if s[i] == "0":
            continue
        number = 0
        j = i
        while j < n:
            number = number * 10 + ord(s[j]) - 48
            if number > k:
                break
            ways[i] = (ways[i] + ways[j + 1]) % MODULUS
            j += 1
    return ways[0]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, zeros):
    out = []
    for i in range(n):
        zero = i > 0 and next_random() % zeros == 0
        out.append("0" if zero else str(1 + next_random() % 9))
    return "".join(out)


def main():
    global seed
    cases = [("1000", 10000), ("1000", 10), ("1317", 2000), ("2020", 30), ("1234567890", 90), ("1", 1), ("10", 9),
             ("1111", 1)]
    print(" ".join(str(number_of_arrays(s, k)) for s, k in cases))
    seed = 1416
    ones = "1" * 100000
    big = drawn(100000, 10)
    f = number_of_arrays
    print(f"10^5 digits: {f(ones, 1000000000)} {f(ones, 1000)} {f(big, 1000000000)} {f(big, 1000)}")
    check = 0
    none = 0
    for i in range(2000):
        n = 1 + next_random() % 40
        s = drawn(n, 2 + next_random() % 8)
        top = [10, 10000, 1000000000][i % 3]
        k = 1 + next_random() % top
        x = f(s, k)
        if x == 0:
            none += 1
        check = (check * 131 + x) % 1000000007
    print(f"2000 random cases: {none} with no array, checksum {check}")


main()
