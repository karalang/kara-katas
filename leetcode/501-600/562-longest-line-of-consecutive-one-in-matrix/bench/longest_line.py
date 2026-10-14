# Benchmark for #562: Python mirror of the ★ arm (one row of running
# counts); see longest_line.kara.


def longest_line(mat):
    n = len(mat[0])
    up = [0] * n
    diag = [0] * n
    anti = [0] * n
    best = 0
    for row in mat:
        next_up = [0] * n
        next_diag = [0] * n
        next_anti = [0] * n
        across = 0
        for j in range(n):
            if row[j] == 1:
                across += 1
                next_up[j] = up[j] + 1
                next_diag[j] = diag[j - 1] + 1 if j > 0 else 1
                next_anti[j] = anti[j + 1] + 1 if j + 1 < n else 1
                best = max(best, across, next_up[j], next_diag[j], next_anti[j])
            else:
                across = 0
        up, diag, anti = next_up, next_diag, next_anti
    return best


# ---- benchmark --------------------------------------------------------------

def main():
    count = 100
    rounds = 100
    seed = 562

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    matrices = []
    m = 1
    for _ in range(count):
        percent = 50 + step() % 46
        matrices.append([[1 if step() % 100 < percent else 0 for _ in range(10000 // m)] for _ in range(m)])
        m = 1 if m == 10000 else m * 10
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            got = longest_line(matrices[(rnd * 7 + g) % count])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} matrices of 10000 cells, {rounds} rounds: total {total}, checksum {checksum}")


main()
