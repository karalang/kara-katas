# LeetCode #1253 bench, in Python: the ★ arm (the 2s counted first, then
# each column of 1 giving its 1 to the upper row while it has room, and
# to the lower after) on 20 random cases of 100000 columns built once,
# each with its own share of 2s and half of them with no matrix; each
# asked 50 times, every answer folded into a checksum.


def reconstruct_matrix(upper, lower, colsum):
    n = len(colsum)
    twos = sum(1 for v in colsum if v == 2)
    ones = sum(1 for v in colsum if v == 1)
    if upper < twos or lower < twos or upper + lower != 2 * twos + ones:
        return []
    up = [0] * n
    low = [0] * n
    left = upper - twos
    for i in range(n):
        if colsum[i] == 2:
            up[i] = 1
            low[i] = 1
        elif colsum[i] == 1:
            if left > 0:
                up[i] = 1
                left -= 1
            else:
                low[i] = 1
    return [up, low]


seed = 1253


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for t in range(20):
        twos = next_random() % 101
        colsum = []
        upper = lower = 0
        for _ in range(100000):
            v = 2 if next_random() % 100 < twos else next_random() % 2
            colsum.append(v)
            if v == 2:
                upper += 1
                lower += 1
            elif v == 1:
                if next_random() % 2 == 0:
                    upper += 1
                else:
                    lower += 1
        if t % 2 == 1:
            upper += 1
        cases.append((upper, lower, colsum))
    check = 0
    for _ in range(50):
        for upper, lower, colsum in cases:
            ans = reconstruct_matrix(upper, lower, colsum)
            even = 0
            if ans:
                i = 0
                while i < len(colsum):
                    even += ans[0][i]
                    i += 2
            check = (check * 131 + len(ans) + even) % 1000000007
    print(f"50 rounds of 20 cases of 100000 columns: checksum {check}")


main()
