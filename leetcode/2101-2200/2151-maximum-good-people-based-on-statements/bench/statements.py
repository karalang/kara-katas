# LeetCode #2151: Maximum Good People Based on Statements -- the
# benchmark's Python mirror of statements.kara.


def maximum_good(statements):
    n = len(statements)
    best = 0
    for mask in range(1 << n):
        holds = True
        for i in range(n):
            if (mask >> i) & 1 == 1:
                for j in range(n):
                    say = statements[i][j]
                    if say != 2 and say != (mask >> j) & 1:
                        holds = False
        if holds:
            best = max(best, bin(mask).count("1"))
    return best


seed = 2151


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 15
    villages = []
    for _ in range(4):
        hidden = next_random() % (1 << n)
        statements = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    say = 2
                elif (hidden >> i) & 1 == 1:
                    say = 2 if next_random() % 3 == 0 else (hidden >> j) & 1
                else:
                    say = next_random() % 3
                row.append(say)
            statements.append(row)
        villages.append(statements)
    total = 0
    check = 0
    for rnd in range(25):
        for v in range(4):
            i = next_random() % n
            j = (i + 1 + next_random() % (n - 1)) % n
            villages[v][i][j] = next_random() % 3
            good = maximum_good(villages[v])
            total += good
            check = (check * 31 + good + rnd) % 1000000007
    print(f"100 solves: {total} good in all, checksum {check}")


main()
