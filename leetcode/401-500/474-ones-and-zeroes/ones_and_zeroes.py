# LeetCode #474: Ones and Zeroes -- Python mirror of the ★ arm
# (ones_and_zeroes.kara): 0/1 knapsack with two budgets, one table.


def count_zeros(s):
    zeros = 0
    for c in s:
        if c == "0":
            zeros += 1
    return zeros


def find_max_form(strs, m, n):
    best = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        zeros = count_zeros(s)
        ones = len(s) - zeros
        for i in range(m, zeros - 1, -1):
            for j in range(n, ones - 1, -1):
                take = best[i - zeros][j - ones] + 1
                if take > best[i][j]:
                    best[i][j] = take
    return best[m][n]


# ---- test harness ---------------------------------------------------------

def show(strs, m, n):
    line = ", ".join(strs)
    print(f"[{line}], m = {m}, n = {n} -> {find_max_form(strs, m, n)}")


seed = 474


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_strs():
    count = 1 + next_random() % 20
    strs = []
    for _ in range(count):
        size = 1 + next_random() % 8
        lean = next_random() % 3
        s = ""
        for _ in range(size):
            r = next_random() % 4
            if lean == 0:
                zero = r != 0
            elif lean == 1:
                zero = r == 0
            else:
                zero = r < 2
            s += "0" if zero else "1"
        strs.append(s)
    return strs


def main():
    show(["10", "0001", "111001", "1", "0"], 5, 3)
    show(["10", "0", "1"], 1, 1)
    show(["10", "0", "1"], 0, 0)
    show(["0", "0", "0", "1"], 2, 0)
    show(["111", "1000", "1000", "1000"], 9, 3)
    show(["00", "000"], 1, 10)
    show(["01", "10", "01", "10", "0011"], 4, 4)
    show(["1"], 0, 1)
    count = 300
    strings = 0
    total = 0
    checksum = 0
    for _ in range(count):
        strs = random_strs()
        m = next_random() % 13
        n = next_random() % 13
        got = find_max_form(strs, m, n)
        strings += len(strs)
        total += got
        checksum = (checksum * 31 + got + 1) % 1000000007
    print(f"{count} random cases, {strings} strings: {total} chosen, checksum {checksum}")


main()
