# LeetCode #1253: Reconstruct a 2-Row Binary Matrix -- the Python mirror of
# reconstruct_matrix.kara: the 2s counted first, then each column of 1
# giving its 1 to the upper row while it has room, and to the lower after.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def judge(upper, lower, colsum, ans):
    if not ans:
        return 0
    n = len(colsum)
    if len(ans) != 2 or len(ans[0]) != n or len(ans[1]) != n:
        return -1
    up = low = 0
    for i in range(n):
        a, b = ans[0][i], ans[1][i]
        if a < 0 or a > 1 or b < 0 or b > 1 or a + b != colsum[i]:
            return -1
        up += a
        low += b
    return 1 if up == upper and low == lower else -1


def random_case(n, twos):
    colsum = []
    upper = lower = 0
    for _ in range(n):
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
    if next_random() % 2 == 0:
        upper += next_random() % 3 - 1
        lower += next_random() % 3 - 1
    return max(upper, 0), max(lower, 0), colsum


def show(v):
    return {1: "matrix", 0: "[]"}.get(v, "WRONG")


def main():
    global seed
    a = judge(2, 1, [1, 1, 1], reconstruct_matrix(2, 1, [1, 1, 1]))
    b = judge(2, 3, [2, 2, 1, 1], reconstruct_matrix(2, 3, [2, 2, 1, 1]))
    cs = [2, 1, 2, 0, 1, 0, 1, 2, 0, 1]
    c = judge(5, 5, cs, reconstruct_matrix(5, 5, cs))
    print(show(a), show(b), show(c))
    seed = 1253
    built = wrong = check = 0
    for t in range(1000):
        n = next_random() % 2000 + 1
        twos = next_random() % 101
        upper, lower, colsum = random_case(n, twos)
        v = judge(upper, lower, colsum, reconstruct_matrix(upper, lower, colsum))
        if v == 1:
            built += 1
        elif v == -1:
            wrong += 1
        check = (check * 131 + v * (t + 1)) % 1000000007
    print(f"1000 random cases: {built} built, {wrong} wrong, checksum {check}")
    twos = [2] * 100000
    ones = [1] * 100000
    x = judge(100000, 100000, twos, reconstruct_matrix(100000, 100000, twos))
    y = judge(50000, 50000, ones, reconstruct_matrix(50000, 50000, ones))
    z = judge(49999, 50000, ones, reconstruct_matrix(49999, 50000, ones))
    print(f"100000 columns: twos {show(x)}, ones {show(y)}, one short {show(z)}")


main()
