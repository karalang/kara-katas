# Benchmark for #474: Python mirror of the ★ arm (0/1 knapsack with two
# budgets, one table); see ones_and_zeroes.kara.


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


seed = 474


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strs = []
    for _ in range(600):
        size = 1 + next_random() % 100
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
    rounds = 300
    total = 0
    checksum = 0
    for _ in range(rounds):
        m = 50 + next_random() % 51
        n = 50 + next_random() % 51
        got = find_max_form(strs, m, n)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{rounds} rounds on 600 strings: {total} chosen, checksum {checksum}")


main()
